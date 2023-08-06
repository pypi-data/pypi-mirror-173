"""Provide scan CLI command."""

import argparse
import itertools
import json
import os
import re
import sys
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, cast, Union

import pydantic.dataclasses
from colorama import Fore, Style
from junitparser import TestSuite, TestCase, Error, JUnitXml, JUnitXmlError, Attr
from pydantic.json import pydantic_encoder

from spotter.api import ApiClient
from spotter.environment import Environment
from spotter.parsing import parse_ansible_artifacts
from spotter.rewriting import Suggestion, update_files
from spotter.storage import Storage


class DisplayLevel(Enum):
    """Enum that holds different levels/statuses for check result."""

    HINT = 1
    WARNING = 2
    # FIXME: Remove this when backward compatibility is needed no more
    WARN = 2
    ERROR = 3

    def __str__(self) -> str:
        """
        Convert DisplayLevel to lowercase string.

        :return: String in lowercase
        """
        return self.name.lower()

    @staticmethod
    def from_string(level: str) -> "DisplayLevel":
        """
        Convert string level to DisplayLevel object.

        :param level: Check result level
        :return: DisplayLevel object
        """
        try:
            return DisplayLevel[level.upper()]
        except KeyError:
            print(f"Error: nonexistent check status display level: {level}, "
                  f"valid values are: {list(str(e) for e in DisplayLevel)}.")
            sys.exit(1)


@pydantic.dataclasses.dataclass
class TaskMetadata:
    """A container for task metadata originating from the original task."""

    file_name: str
    task_line: str
    task_column: str

    @classmethod
    def from_task_meta(cls, task_meta: Dict[str, Any]) -> "TaskMetadata":
        """
        Create TaskMetadata object for storing metadata for Ansible task.

        :param task_meta: Ansible task spotter_metadata content.
        :return: TaskMetadata object
        """
        file_name = task_meta.get("file", "")
        task_line = task_meta.get("line", "")
        task_column = task_meta.get("column", "")

        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        return cls(
            file_name=file_name,
            task_line=task_line,
            task_column=task_column
        )


@pydantic.dataclasses.dataclass
class CheckCatalogInfo:
    """A container for information about the specific check in check catalog from the backend."""

    event_code: str
    event_value: str
    event_message: str
    check_class: str


@pydantic.dataclasses.dataclass
class CheckResult:
    """A container for parsed check results originating from the backend."""

    task_id: str
    original_task: Dict[str, Any]
    task_metadata: TaskMetadata
    catalog_info: CheckCatalogInfo
    level: DisplayLevel
    message: str
    suggestion: Optional[Suggestion]
    doc_url: Optional[str]

    def construct_output(self, disable_colors: bool = False, disable_docs_url: bool = False) -> str:
        """
        Construct CheckResult output using its properties.

        :param disable_colors: Disable output colors and styling
        :param disable_docs_url: Disable outputting URL to documentation
        :return: Formatted output for check result
        """
        task_metadata = self.task_metadata

        result_level = self.level.name.strip().upper()
        out_prefix = f"{task_metadata.file_name}:{task_metadata.task_line}:{task_metadata.task_column}: {result_level}"
        out_message = self.message.strip()
        if not disable_colors:
            if result_level == DisplayLevel.ERROR.name:
                out_prefix = Fore.RED + out_prefix + Fore.RESET
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + Fore.RED + r"\1" + Fore.RESET + Style.NORMAL,
                                     out_message)
            elif result_level == DisplayLevel.WARNING.name:
                out_prefix = Fore.YELLOW + out_prefix + Fore.RESET
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + Fore.YELLOW + r"\1" + Fore.RESET + Style.NORMAL,
                                     out_message)
            else:
                out_message = re.sub(r"'([^']*)'", Style.BRIGHT + r"\1" + Style.NORMAL, out_message)

        output = f"{out_prefix}: {out_message}".strip()
        if not output.endswith("."):
            output += "."
        if not disable_docs_url and self.doc_url:
            output = f"{output} View docs at {self.doc_url}."

        return output


def add_parser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore
    """
    Add a new parser to subparsers.

    :param subparsers: Subparsers action
    """
    parser = subparsers.add_parser(
        "scan", help="Initiate Ansible scan", description="Initiate Ansible scan"
    )
    parser.add_argument(
        "--project-id", "-t", type=str, help="UUID of an existing project (default project from "
                                             "personal organization will be used if not specified)",
    )
    parser.add_argument(
        "--config", "-c", type=lambda p: Path(p).absolute(), help="Configuration file (as JSON/YAML)"
    )
    parser.add_argument(
        "--option", "-o", type=lambda s: s.strip().split("="), action="append", default=[],
        help="Additional config variable as key=value pair, for example ansible_version=2.13"
    )
    parser.add_argument(
        "--upload-values", action="store_true",
        help="Parse and upload values from Ansible task parameters",
    )
    parser.add_argument(
        "--parse-values", "-p", dest="upload_values", action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--upload-metadata", action="store_true",
        help="Upload metadata (i.e., file names, line and column numbers) to portal",
    )
    parser.add_argument(
        "--rewrite", "-r", action="store_true", help="Rewrite files with fixes",
    )
    parser.add_argument(
        "--display-level", "-l", type=DisplayLevel.from_string,
        choices=list(DisplayLevel), default=DisplayLevel.HINT,
        help="Display only check results with specified level or greater "
             "(e.g., -l warning will show all warnings and errors, but suppress hints)"
    )
    parser.add_argument(
        "--no-docs-url", action="store_true", help="Disable outputting URL to documentation"
    )
    parser.add_argument(
        "--junit-xml", "-j", type=lambda p: Path(p).absolute(),
        help="Output file path to export the scan result to a file in JUnit XML format"
    )
    import_export_group = parser.add_mutually_exclusive_group()
    import_export_group.add_argument(
        "--import-payload", "-i", type=lambda p: Path(p).absolute(),
        help="Path to the previously exported file to be sent for scanning"
    )
    import_export_group.add_argument(
        "--export-payload", "-e", type=lambda p: Path(p).absolute(),
        help="Output file path to export the locally scanned data without sending anything for scanning at the server"
    )
    import_export_group.add_argument(
        "--export-payload-raw", type=lambda p: Path(p).absolute(),
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        "path", type=lambda p: Path(p).absolute(), nargs="*", help="Path to Ansible artifact or directory",
    )
    parser.set_defaults(func=_parser_callback)


def _parser_callback(args: argparse.Namespace) -> None:
    # pylint: disable=too-many-branches,too-many-locals, too-many-statements
    """
    Invoke the Ansible scanner and print/save the scan result (parser callback function).

    :param args: Argparse arguments
    """
    username = args.username or os.environ.get("SPOTTER_USERNAME")
    password = args.password or os.environ.get("SPOTTER_PASSWORD")
    storage = Storage.create(args.storage_path)
    client = ApiClient(ApiClient.ENDPOINT, storage, username, password)
    scan_paths = args.path

    if args.import_payload and scan_paths:
        print("Error: the --import-payload is mutually exclusive with positional arguments.")
        sys.exit(1)

    if args.export_payload and not scan_paths or (
            not args.export_payload and not args.import_payload and not scan_paths):
        print("Error: no paths provided for scanning.")
        sys.exit(1)

    # create and set environment
    # the order that we read configuration is the following (in each step we overwrite what the previous one has):
    # 1. local discovery (from user's current workspace)
    # 2. config file (JSON/YAML file provided after --config flag)
    # 3. options provided as key=value pairs to the scan command
    environment = Environment.from_local_discovery(scan_paths)
    if args.config:
        environment = environment.combine(Environment.from_config_file(args.config))
    if args.option:
        extra_vars = {}
        for key_value in args.option:
            if len(key_value) != 2:
                print(f"Error: '{'='.join(key_value)}' extra option is not specified as key=value.")
                sys.exit(1)
            else:
                extra_vars[key_value[0]] = key_value[1]

        environment = environment.combine(Environment.from_extra_vars(extra_vars))

    if args.import_payload:
        environment, input_tasks, input_playbooks = _import_scan_payload_from_json_file(args.import_payload)
    else:
        input_tasks = []
        input_playbooks = []
        if scan_paths:
            input_tasks, input_playbooks = parse_ansible_artifacts(scan_paths, parse_values=bool(args.upload_values))

    cli_scan_args = {
        "parse_values": args.upload_values,  # deprecated - but currently mandatory on backend
        "upload_values": args.upload_values,
        "upload_metadata": args.upload_metadata,
        "rewrite": args.rewrite,
        "display_level": str(args.display_level)
    }
    environment.cli_scan_args = cli_scan_args

    if args.export_payload_raw:
        tasks = input_tasks if args.upload_metadata else _remove_sensitive_data_from_tasks(input_tasks)
        playbooks = input_playbooks if args.upload_metadata else _remove_sensitive_data_from_playbooks(input_playbooks)
        scan_payload = {"environment": pydantic_encoder(environment),
                        "tasks": tasks,
                        "playbooks": playbooks
                        }

        _export_scan_payload_to_json_file(scan_payload, args.export_payload_raw)

        file_name = str(args.export_payload_raw)
        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        print(f"Scan data saved to {file_name}.\nNote: this operation is fully offline. No actual scan was executed.")
        sys.exit(0)

    if args.export_payload:
        scan_payload = {
            "environment": pydantic_encoder(environment),
            "tasks": input_tasks,
            "playbooks": input_playbooks
        }

        _export_scan_payload_to_json_file(scan_payload, args.export_payload)

        file_name = str(args.export_payload)
        try:
            # trim the part of the directory that is shared with CWD if this is possible
            file_name = str(Path(file_name).relative_to(Path.cwd()))
        except ValueError:
            pass

        print(f"Scan data saved to {file_name}.\nNote: this operation is fully offline. No actual scan was executed.")
    else:
        tasks = input_tasks if args.upload_metadata else _remove_sensitive_data_from_tasks(input_tasks)
        playbooks = input_playbooks if args.upload_metadata else _remove_sensitive_data_from_playbooks(input_playbooks)
        scan_payload = {"environment": pydantic_encoder(environment),
                        "tasks": tasks,
                        "playbooks": playbooks
                        }

        if args.project_id:
            response = client.post(f"/v2/scans/?project={args.project_id}", payload=scan_payload, timeout=120)
        else:
            response = client.post("/v2/scans/", payload=scan_payload, timeout=120)

        check_results_all = parse_check_results(input_tasks, response.json())
        check_results_filtered = filter_check_results(check_results_all, args.display_level)

        if args.junit_xml:
            export_check_results_junit_xml(check_results_filtered, args.junit_xml, args.no_docs_url)
            print(f"Scan result exported to {args.junit_xml} in JUnit XML format.")
            sys.exit(0)
        else:
            print_check_results(check_results_filtered, args.no_colors, args.no_docs_url)

            if args.rewrite:
                apply_check_result_suggestions(check_results_filtered, scan_paths)

            if len(check_results_filtered) > 0:
                sys.exit(1)


def _import_scan_payload_from_json_file(import_path: Path) -> \
        Tuple[Environment, List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Import scan input from JSON file.

    :param import_path: File path to import from (must exist)
    :return: Scan input tuple (environment, tasks, playbooks)
    """
    try:
        if not import_path.exists():
            print(f"Error: import file at {import_path} does not exist.")
            sys.exit(1)

        with import_path.open("r") as import_file:
            scan_payload = json.load(import_file)
            environment_dict = scan_payload.get("environment", None)
            if environment_dict is not None:
                environment = Environment(**environment_dict)
            else:
                environment = Environment()

            return environment, scan_payload.get("tasks", []), scan_payload.get("playbooks", [])
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def _export_scan_payload_to_json_file(scan_payload: Dict[str, Any], export_path: Path) -> None:
    """
    Export scan input to JSON file.

    :param scan_payload: Scan input as dict
    :param export_path: File path to export to (will be overwritten if exists)
    """
    try:
        with export_path.open("w") as export_file:
            json.dump(scan_payload, export_file, indent=2)
    except TypeError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


def _remove_sensitive_data_from_tasks(input_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove sensitive data from input tasks.

    :param input_tasks: Input Ansible task list
    :return: Cleaned list of input tasks
    """
    return [
        {
            "task_id": t["task_id"],
            "task_args": t["task_args"]
        } for t in input_tasks
    ]


def _remove_sensitive_data_from_playbooks(input_playbooks: List[Dict[str, Any]]) -> \
        List[Dict[str, Union[str, List[Dict[str, Any]]]]]:
    """
    Remove sensitive data from input playbooks.

    :param input_playbooks: Input Ansible playbooks list
    :return: Cleaned list of input playbooks
    """
    return [
        {
            "playbook_id": t["playbook_id"],
            "plays": [
                {
                    "play_id": x.get("play_id", None),
                    "play_args": x["play_args"]
                }
                for x in t["plays"]
            ]
        } for t in input_playbooks
    ]


def parse_check_results(input_tasks: List[Dict[str, Any]], scan_output: Dict[str, Any]) -> List[CheckResult]:
    """
    Parse result objects and map tasks with complete information.

    :param input_tasks: The scanned tasks with no information removed
    :param scan_output: The backend API response
    :return: A list of check results
    """
    result: List[CheckResult] = []

    for element in scan_output.get("elements", []):
        task_id = element.get("task_id", "")
        suggestion = element.get("suggestion", "")

        # match the result task's ID to the original task (with complete information)
        original_task: Optional[Dict[str, Any]] = None
        for task in input_tasks:
            if task.get("task_id", None) == task_id:
                original_task = task
                break

        # guard against incomplete results where we don't match a task
        if original_task is None:
            print("Could not map task ID to its original task.")
            continue

        # guard against missing task args and metadata
        task_meta = original_task.get("spotter_metadata", None)
        if task_meta:
            task_metadata_object = TaskMetadata.from_task_meta(task_meta)
            suggestion_object: Optional[Suggestion] = None
            if suggestion:
                suggestion_object = Suggestion.from_task(original_task, suggestion)

            result.append(
                CheckResult(task_id, original_task, task_metadata_object,
                            CheckCatalogInfo(element.get("event_code", ""), element.get("event_value", ""),
                                             element.get("event_message", ""), element.get("check_class", "")),
                            DisplayLevel.from_string(element.get("level", "")), element.get("message", ""),
                            suggestion_object, element.get("doc_url", ""))
            )

    return result


def filter_check_results(results: List[CheckResult], threshold: DisplayLevel) -> List[CheckResult]:
    """
    Filter a list of results by only keeping tasks over a specified severity level.

    :param results: The list of results to filter
    :param threshold: The threshold (inclusive) of what level messages (and above) to keep
    :return: A filtered list of results
    """
    return [cr for cr in results if cr.level.value >= threshold.value]


def print_check_results(results: List[CheckResult], disable_colors: bool = False,
                        disable_docs_url: bool = False) -> None:
    """
    Render a list of results into the console (assumes results are pre-filtered).

    :param results: The results to display
    :param disable_colors: Disable output colors and styling
    :param disable_docs_url: Disable outputting URL to documentation
    """
    for result in results:
        print(result.construct_output(disable_colors, disable_docs_url))

    if len(results) > 0:
        def level_sort_key(level: DisplayLevel) -> int:
            return cast(int, level.value)

        worst_level = max((cr.level for cr in results), key=level_sort_key)

        print("------------------------------------------------------------------------")

        overall_status_message = f"Overall status: {worst_level.name.upper()}"
        if not disable_colors:
            overall_status_message = Style.BRIGHT + overall_status_message
        print(overall_status_message)


def export_check_results_junit_xml(results: List[CheckResult], export_path: Path,
                                   disable_docs_url: bool = False) -> None:
    """
    Render a list of results into the console (assumes results are pre-filtered).

    :param results: The results to display
    :param export_path: File path to export JUnit XML to (will be overwritten if exists)
    :param disable_docs_url: Disable outputting URL to documentation
    """
    try:
        # add custom attributes for JUnit XML schema
        TestCase.file = Attr("file")

        xml = JUnitXml()
        get_check_class = lambda res: res.catalog_info.check_class  # pylint: disable=unnecessary-lambda-assignment
        for check_class, check_results in itertools.groupby(sorted(results, key=get_check_class), get_check_class):
            suite = TestSuite(check_class)
            check_count = 0

            for result in check_results:
                test_case = TestCase(
                    f"{result.catalog_info.event_code}-{result.catalog_info.event_value}[{check_count}]", check_class
                )
                test_case.id = result.catalog_info.event_code
                test_case.file = result.task_metadata.file_name
                test_case.result = [Error(result.construct_output(True, disable_docs_url), result.level.name.upper())]

                suite.append(test_case)
                check_count += 1

            suite.tests = check_count
            suite.errors = check_count
            xml.add_testsuite(suite)

        xml.write(export_path)
    except JUnitXmlError as e:
        print(f"Error exporting JUnit XML: {e}.")
        sys.exit(1)


def apply_check_result_suggestions(results: List[CheckResult], scan_paths: List[Path]) -> None:
    """
    Automatically apply suggestions.

    :param results: A list of results, which may or may not contain suggestions, to apply suggestions from
    :param scan_paths: A list of original paths to Ansible artifacts provided for scanning
    """
    all_suggestions = [cr.suggestion for cr in results if cr.suggestion is not None]

    # TODO: Remove this when we find a solution for accessing original paths to Ansible artifacts provided for scanning
    for suggestion in all_suggestions:
        suggestion.file_parent = suggestion.file.parent
        for scan_path in scan_paths:
            if scan_path in (scan_path / suggestion.file).parents:
                suggestion.file_parent = scan_path
                break

    update_files(all_suggestions)
