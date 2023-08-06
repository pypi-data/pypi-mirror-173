from ..pypiprocess import PYPIProcess
from .. import constants as _constants


def __get_task(__system_args: dict[str, dict], default: str = "create"):

    task = next(
        (key for key in __system_args.keys() if key in _constants.CLI_COMMANDS),
        default,
    )
    if task and task in __system_args:
        del __system_args[task]
    return task


def __get_package_process_kwargs(__system_args: dict[str, dict], __field_ids):
    kwargs = dict(task=__get_task(__system_args))
    for field_id in __field_ids:
        if not field_id in kwargs and field_id in __system_args:
            kwargs[field_id] = __system_args[field_id]["value"]
    return kwargs


def __init_pypiprocess(__system_args: dict[str, dict]):

    kwargs = __get_package_process_kwargs(__system_args, PYPIProcess.__fields__.keys())
    return PYPIProcess(**kwargs)


def init_pypiprocess(__system_args: dict[str, dict]):
    return __init_pypiprocess(__system_args)
