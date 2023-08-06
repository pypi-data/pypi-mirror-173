from ...pypipackage import PYPIPackage
from ...utils import util as _util


def init_build_subconfig(kwargs: dict = None):
    if kwargs is not None:
        kwargs_ = {key: "" if value is None else value for key, value in kwargs.items()}
        result = PYPIPackage.Config.Build(**kwargs_)
    else:
        result = PYPIPackage.Config.Build()
    if isinstance(result.autoinstall, str):
        result.autoinstall = _util.str_is_true(result.autoinstall)
    if isinstance(result.build_files, str):
        result.build_files = _util.str_is_true(result.build_files)
    return result


def init_package_subconfig(kwargs: dict = None):
    _kwargs = {} if kwargs is None else kwargs
    result = PYPIPackage.Config.Package(**_kwargs)
    print(_kwargs)
    result.parentdir = _util.format_parentdir(result.parentdir, result.name)
    return result


def init_pypi_subconfig(kwargs: dict = None):
    kwargs_ = {} if kwargs is None else kwargs
    result = PYPIPackage.Config.PYPI(**kwargs_)
    return result
