import sys as _sys
from typing import List, Callable
import osiotk as _os
from . import objects
from . import tasks
from . import init as _init
from .pydantic_model import PydanticModel, Field


class _SystemArg(PydanticModel):

    index: int = Field(0)
    arg: str = Field("")
    type: str = Field("")
    name: str = Field("")
    value: str = Field("")


class LazyData(PydanticModel):

    value: (dict[str, dict] | None) = Field(None)
    is_initialized: bool = Field(False)

    def getvalue(self, fetch: Callable):
        value = self.value
        if not self.is_initialized:
            value = fetch()
            self.value = value
            self.is_initialized = True
        return value


def __init_systemarg(kwargs: dict = None, asdict: bool = False):
    kwargs_ = {} if kwargs is None else kwargs
    result = _SystemArg(**kwargs_)
    result.value = result.arg
    if "=" in result.arg:
        nv = result.arg.split("=", 1)
        result.name, result.value = nv[0], nv[1]
    else:
        result.name = result.arg
    if asdict:
        result = result.dict()
    return result


def __load_systemargs(args: List[str] = None):

    argv = _sys.argv if args is None else args
    return {
        system_arg["name"]: system_arg
        for system_arg in (
            __init_systemarg(kwargs=dict(index=index, arg=arg), asdict=True)
            for (index, arg) in enumerate(argv)
        )
        if system_arg["name"]
    }


system_args_data = LazyData()


def __init_system_args(args: List[str] = None):
    def fetch():
        return __load_systemargs(args=args)

    result = system_args_data.getvalue(fetch=fetch)
    assert isinstance(result, dict), __name__ + f" system args is not dict"
    return result


def init_system_args(args: List[str] = None):

    return __init_system_args(args=args)


def __execute_runtime(__runtime: objects.PYPIRuntime):
    __task = __runtime.process.task
    if __task == "create":
        tasks.build(__runtime.package)
    elif __task == "update":
        tasks.update(__runtime.package)
    elif __task == "help":
        print("task=help")


def __postprocess_runtime(__runtime: objects.PYPIRuntime):
    parentdir = __runtime.package.config.package.parentdir
    commands = []
    if __runtime.process.open_in_finder:
        commands.append(f"open {parentdir}")
    if __runtime.process.open_in_vscode:
        commands.append(f"code {parentdir}")
    for command in commands:
        _os.system(command)


def __ensure_system_args(__system_args: dict[str, dict] = None):
    if __system_args is None:
        __system_args = __init_system_args()
    return __system_args


def __init_runtime(__system_args: dict[str, dict] = None):

    system_args = __ensure_system_args(__system_args)
    process = _init.init_pypiprocess(system_args)
    package = _init.init_pypipackage(system_args=system_args)
    return objects.PYPIRuntime(
        package=package, process=process, system_args=system_args
    )


def init_runtime(__system_args: dict[str, dict] = None):
    return __init_runtime(__system_args)


def execute(__runtime: objects.PYPIRuntime):
    __execute_runtime(__runtime)


def postprocess(__runtime: objects.PYPIRuntime):
    return __postprocess_runtime(__runtime)


def run(__system_args: dict[str, dict] = None):
    pypiruntime = __init_runtime(__system_args)
    __execute_runtime(pypiruntime)
    postprocess(pypiruntime)
