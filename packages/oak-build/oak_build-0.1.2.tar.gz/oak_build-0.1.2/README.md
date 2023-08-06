# oak-build

A make-like build system written on python


## How to use

Create `oak_build.py` file in your project directory.
Every method marked with `@task` decorator can be called from CLI.

```python
from pathlib import Path

from oak_build import task


@task
def create_file():
    with open(Path("result.txt"), "w") as txt:
        txt.write("test content\n")
```

To execute `create_file` task call `oak create_file` from console.

## Task dependencies

You can link dependent tasks with `depends_on` parameter.

```python
from oak_build import task, run


@task
def unit_tests():
    run("poetry run pytest tests")


@task
def integration_tests():
    run("poetry run pytest integration_tests")


@task(
    depends_on=[
        unit_tests,
        integration_tests,
    ]
)
def tests():
    pass
```

When `oak tests` is called oak build will execute `unit_tests` and `integration_tests` tasks as well.

## CLI params

You can pass parameters to tasks with `--param key=value` parameter of command line.
Oak will try to parse all task function params regarding its annotation type.

Example:

```python
from enum import Enum, auto
from oak_build import task


class TaskEnum(Enum):
    VALUE = auto()


@task
def enum_param(param: TaskEnum):
    pass
```

## Task results

### Exit code

All int return value from task will be treated as return code.
If return is integer and not zero task will be marked as failed and further execution will be stopped.

```python
from oak_build import task

@task
def exit_code_task():
    return 0
```

### Result dict

All dict return value will be treated as result.
Those results can be used in another tasks with tas name prefix (see example below).

```python
from oak_build import task

@task
def source():
    return {
        "result": 123,
    }

@task(depends_on=[source])
def result_consumer(source_result):
    pass
```

Please note that CLI params have greater priority than arguments deducted from task results.

### Code and result

You can return `Tuple[int, Dict[str, Any]]` from task, and it will be treated as return code and result dict.
If code is not zero task is considered failed.
The result dict processing is the same as in dict result

### Exceptions

If task throws exception it is considered faled and further execution will be stopped.


## Examples

For examples see [integration tests files](integration_tests/resources) and self build [oak_file.py](oak_file.py).
