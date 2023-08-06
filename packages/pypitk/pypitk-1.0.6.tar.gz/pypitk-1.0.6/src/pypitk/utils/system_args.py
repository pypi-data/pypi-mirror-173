import sys as _sys
from typing import List, Callable
from ..pydantic_model import PydanticModel, Field


class SystemArg(PydanticModel):

    index: int = Field(0)
    arg: str = Field("")
    type: str = Field("")
    name: str = Field("")
    value: str = Field("")


class SystemArgs(dict[str, SystemArg]):
    def list(self, reverse: bool = False):
        result = list(self.values())
        result.sort(key=lambda system_arg: system_arg.index, reverse=reverse)
        return result

    def index(self, i: int):
        return self.list()[i]

    @classmethod
    def init(cls, args: List[str] = None):
        argv = _sys.argv if args is None else args
        return cls(
            {
                system_arg.name: system_arg
                for system_arg in (
                    SystemArg.init(kwargs=dict(index=index, arg=arg))
                    for (index, arg) in enumerate(argv)
                )
                if system_arg.name
            }
        )

    def __iter__(self):
        return iter(self.values())


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


def __init_systemarg(kwargs: dict = None):
    kwargs_ = {} if kwargs is None else kwargs
    result = SystemArg(**kwargs_)
    result.value = result.arg
    if "=" in result.arg:
        nv = result.arg.split("=", 1)
        result.name, result.value = nv[0], nv[1]
    else:
        result.name = result.arg
    return result


__init_systemarg_dict = lambda kwargs: __init_systemarg(kwargs).dict()


def __list_systemargs(__systemargs: dict[str, dict], reverse: bool = False):
    result = list(__systemargs.values())
    result.sort(key=lambda system_arg: system_arg.get("index", 0), reverse=reverse)
    return result


def list_systemargs(__systemargs: dict[str, dict], reverse: bool = False):
    return __list_systemargs(__systemargs, reverse=reverse)


def get_systemarg(__systemargs: dict[str, dict], i: int = None):
    if i is not None:
        result = list_systemargs(__systemargs)[i]
    else:
        result = None
    return result


def __init_systemargs(args: List[str] = None):

    argv = _sys.argv if args is None else args
    return {
        system_arg["name"]: system_arg
        for system_arg in (
            __init_systemarg_dict(kwargs=dict(index=index, arg=arg))
            for (index, arg) in enumerate(argv)
        )
        if system_arg["name"]
    }


data = LazyData()


def init_system_args(args: List[str] = None):
    def fetch():
        return __init_systemargs(args=args)

    result = data.getvalue(fetch=fetch)
    assert isinstance(result, dict), __name__ + f" system args is not dict"
    return result
