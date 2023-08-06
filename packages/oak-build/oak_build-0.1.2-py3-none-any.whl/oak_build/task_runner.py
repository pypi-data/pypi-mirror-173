from collections import OrderedDict
from dataclasses import dataclass
from enum import Enum
from inspect import signature, Signature
from typing import List, Dict, Any, Callable, Optional

from rusty_results import Result, Err, Ok
from toposort import toposort_flatten

from oak_build.direcory_exec_context import DirectoryExecContext
from oak_build.oak_file import OakFile
from oak_build.parsers import parse_str, parse_int, parse_bool, parse_enum

DUMMY = 0


def unify_task_name(name: str):
    return name.replace("-", "_")


@dataclass
class TaskResult:
    exit_code: int
    exit_params: Dict
    error: Optional[Exception]


class TaskRunner:
    def run_tasks(
        self, oak_file: OakFile, params: Dict[str, str], tasks: List[str]
    ) -> Result[None, List[str]]:
        tasks = [unify_task_name(t) for t in tasks]
        known_tasks = set(oak_file.tasks.keys()).union(oak_file.aliases.keys())

        errors = []
        for task in tasks:
            if task not in known_tasks:
                errors.append(f"Unknown task {task}")
        if errors:
            return Err(errors)

        tasks_to_run = self._deduct_tasks_to_run(oak_file, tasks)
        arguments = {}
        with DirectoryExecContext(oak_file.path.parent):
            for task in tasks_to_run:
                task_result = self.run_task(
                    task, oak_file.tasks[task], oak_file.context, arguments, params
                )
                if task_result.exit_code == 0:
                    arguments.update(
                        {
                            f"{task}_{key}": value
                            for key, value in task_result.exit_params.items()
                        }
                    )
                elif task_result.error is None:
                    return Err(
                        [f"Task {task} failed with exit code {task_result.exit_code}"]
                    )
                else:
                    return Err(
                        [f"Task {task} failed with exception {task_result.error}"]
                    )
            return Ok(None)

    @staticmethod
    def _deduct_tasks_to_run(oak_file: OakFile, tasks: List[str]) -> List[str]:
        edges = {}

        for dependant, dependencies in oak_file.dependencies.items():
            edges[dependant] = set(dependencies)

        result = OrderedDict()

        def recursive_append(target: Dict, source: Dict, key: Any):
            if key in source:
                target[key] = source[key]
                for x in target[key]:
                    if x not in target.keys():
                        recursive_append(target, source, x)

        for task in tasks:
            # Here we create subset of all dependencies that includes only selected tasks and its dependencies
            dependencies_subset = {}
            recursive_append(dependencies_subset, edges, task)
            task_required = toposort_flatten(dependencies_subset)
            for x in task_required:
                result[x] = DUMMY

        return list(result.keys())

    def run_task(
        self,
        task_name: str,
        task_callable: Callable,
        context: Dict,
        arguments: Dict,
        parameters: Dict,
    ):
        """
        :param task_name: task name
        :param task_callable: task callable
        :param context: global task context
        :param arguments: arguments build as task results
        :param parameters: str parameters fro cli
        :return:
        """
        sig = signature(task_callable)
        locals_values = {}
        for arg in sig.parameters:
            if arg in parameters:
                parser = TaskRunner.get_argument_parser(sig.parameters[arg].annotation)
                result = parser(parameters.get(arg))
                if result.is_ok:
                    locals_values[arg] = result.unwrap()
                else:
                    return TaskResult(
                        1,
                        {},
                        ValueError(
                            f"Cannot parse parameter {arg} of {task_name} because of {result.unwrap_err()}"
                        ),
                    )
            elif arg in arguments:
                locals_values[arg] = arguments[arg]

        exception = None
        try:
            exec(
                f'RESULT = {task_name}({", ".join(locals_values.keys())})',
                context,
                locals_values,
            )
        except Exception as e:
            exception = e
        res = locals_values.get("RESULT")

        if exception is not None:
            return TaskResult(1, {}, exception)
        elif res is None:
            return TaskResult(0, {}, None)
        elif isinstance(res, int):
            return TaskResult(res, {}, None)
        elif isinstance(res, dict):
            return TaskResult(0, res, None)
        elif (
            isinstance(res, tuple)
            and (len(res) == 2)
            and isinstance(res[0], int)
            and isinstance(res[1], dict)
        ):
            return TaskResult(res[0], res[1], None)
        else:
            return TaskResult(
                1,
                {},
                Exception(
                    f"Incorrect return type for task {task_name}. Must be int, dict or tuple(int, dict)"
                ),
            )

    @staticmethod
    def get_argument_parser(annotation) -> Callable[[str], Result]:
        if annotation is Signature.empty:
            return lambda value: Ok(value)
        elif annotation is str:
            return parse_str
        elif annotation is bool:
            return parse_bool
        elif annotation is int:
            return parse_int
        elif issubclass(annotation, Enum):
            return lambda value: parse_enum(value, annotation)
        else:
            return lambda value: annotation(value)
