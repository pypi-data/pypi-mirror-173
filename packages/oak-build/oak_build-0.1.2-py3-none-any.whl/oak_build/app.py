import logging

from pathlib import Path
from typing import List, Dict
from argparse import ArgumentParser, REMAINDER

from rusty_results import Result, Ok, Err

from oak_build.app_logging import DEFAULT_LEVEL, LEVELS, init_logging
from oak_build.oak_file import DEFAULT_OAK_FILE, OakFileLoader
from oak_build.task_runner import TaskRunner


class App:
    def __init__(self, args: List[str]):
        parser = App._init_arg_parser()
        parsed_args = parser.parse_args(args)

        init_logging(parsed_args.log_level)

        logging.debug(f"Parsed arguments are {parsed_args}")

        self.oak_file: Path = parsed_args.file
        self.tasks: List[str] = parsed_args.tasks
        self.params: List[str] = parsed_args.param

    def run(self) -> int:
        params = self._parse_params(self.params)
        if params.is_err:
            for error in params.unwrap_err():
                logging.error(error)
            return 1

        file_description = OakFileLoader.load_file(self.oak_file)
        if file_description.is_err:
            for error in file_description.unwrap_err():
                logging.error(error)
            return 1

        run_result = TaskRunner().run_tasks(
            file_description.unwrap(), params.unwrap(), self.tasks
        )
        if run_result.is_err:
            for error in run_result.unwrap_err():
                logging.error(error)
            return 1
        return 0

    @staticmethod
    def _init_arg_parser() -> ArgumentParser:
        parser = ArgumentParser(
            prog="oak",
        )
        parser.add_argument("-l", "--log-level", default=DEFAULT_LEVEL, choices=LEVELS)
        parser.add_argument("-f", "--file", default=DEFAULT_OAK_FILE, type=Path)
        parser.add_argument(
            "-p", "--param", action="append", default=[], help="Script parameters"
        )
        parser.add_argument("tasks", nargs=REMAINDER)
        return parser

    @staticmethod
    def _parse_params(params: List[str]) -> Result[Dict[str, str], List[str]]:
        result = {}
        errors = []
        for param in params:
            kv_pair = param.split("=", maxsplit=1)
            if len(kv_pair) == 2:
                result[kv_pair[0]] = kv_pair[1]
            else:
                errors.append(f"Cannot parse {param} as key=value pair")
        if not errors:
            return Ok(result)
        else:
            return Err(errors)
