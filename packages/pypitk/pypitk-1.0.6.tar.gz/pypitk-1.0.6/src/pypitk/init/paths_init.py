import osiotk as _os
from ..pypipackage import PYPIPackage
from ..utils import util as _util
from .. import constants as _constants


def __init_paths_base(parentdir: str, package_name: str):
    parentdir = _util.format_package_path(package_name, path=parentdir)
    joinpath = lambda __name: _util.format_package_path(
        package_name, _os.join_paths(parentdir, __name)
    )

    constant_kwargs = {
        path_id: f"FILENAME_{path_id.upper()}"
        for path_id in PYPIPackage.Data.__fields__.keys()
    }
    constant_data = {
        path_id: getattr(_constants, constant_id)
        for path_id, constant_id in constant_kwargs.items()
    }
    kwargs = {
        path_id: joinpath(path_data) for path_id, path_data in constant_data.items()
    }
    return PYPIPackage.Paths(**kwargs)


def __init_paths_from_package(__package: PYPIPackage.Config.Package):
    parentdir = __package.parentdir
    name = __package.name
    return __init_paths_base(parentdir=parentdir, package_name=name)


def __init_paths_from_config(__config: PYPIPackage.Config):
    package = __config.package
    return __init_paths_from_package(package)


def init_paths_base(parentdir: str, package_name: str):
    return __init_paths_base(parentdir, package_name)


def init_paths_from_package(__package: PYPIPackage):
    return __init_paths_from_package(__package)


def init_from_config(__config: PYPIPackage.Config):
    return __init_paths_from_config(__config)
