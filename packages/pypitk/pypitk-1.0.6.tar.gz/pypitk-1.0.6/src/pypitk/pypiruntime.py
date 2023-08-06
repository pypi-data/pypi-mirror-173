import osiotk as _os
from . import build_pypipackage as _build_package
from . import update_pypipackage as _update_package
from .utils import system_args as _system_args
from .init import pypipackage_init, pypiprocess_init
from . import pypiprocess, pypipackage
from .pydantic_model import PydanticModel, Field


class PYPIRuntime(PydanticModel):

    package: pypipackage.PYPIPackage = Field()
    process: pypiprocess.PYPIProcess = Field()
    system_args: dict[str, dict] = Field()


def __execute_runtime(__runtime: PYPIRuntime):
    __task = __runtime.process.task
    if __task == "create":
        _build_package.build_package(__runtime.package)
    elif __task == "update":
        _update_package.update_package(package=__runtime.package)
    elif __task == "help":
        print("task=help")


def __postprocess_runtime(__runtime: PYPIRuntime):
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
        __system_args = _system_args.init_system_args()
    return __system_args


def __init_runtime(__system_args: dict[str, dict] = None):

    system_args = __ensure_system_args(__system_args)
    process = pypiprocess_init.init_pypiprocess(system_args)
    package = pypipackage_init.init_pypipackage(system_args=system_args)
    return PYPIRuntime(package=package, process=process, system_args=system_args)


def init_runtime(__system_args: dict[str, dict] = None):
    return __init_runtime(__system_args)


def execute(__runtime: PYPIRuntime):
    __execute_runtime(__runtime)


def postprocess(__runtime: PYPIRuntime):
    return __postprocess_runtime(__runtime)
