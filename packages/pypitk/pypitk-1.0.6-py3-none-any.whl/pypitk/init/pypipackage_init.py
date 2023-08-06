from src.pypitk.pypipackage import PYPIPackage
from . import config_init as _config_init
from . import content_init as _content_init
from . import paths_init as _paths_init
from .. import constants as _constants
from ..utils import util as _util


def __postinit_pypackage_config(__pypipackage: PYPIPackage):
    __pypipackage.config.package.name = _util.format_package_name(
        __pypipackage.config.package.name
    )
    __pypipackage.config.package.parentdir = _util.format_package_path(
        __pypipackage.config.package.name, __pypipackage.config.package.parentdir
    )
    return __pypipackage


def __postinit_pypackage_filenames(__pypipackage: PYPIPackage):
    for content_path_key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
        path = getattr(__pypipackage.paths, content_path_key)
        formatted_path = _util.format_package_path(
            __pypipackage.config.package.name, path
        )
        setattr(__pypipackage.paths, content_path_key, formatted_path)
    return __pypipackage


def __postinit_pypipackage(__pypipackage: PYPIPackage):
    __pypipackage = __postinit_pypackage_config(__pypipackage)
    __pypipackage = __postinit_pypackage_filenames(__pypipackage)

    __pypipackage.content.pypitk_package = __pypipackage.json(indent=4)

    return __pypipackage


def __init_pypipackage_from_config(__config):
    paths = _paths_init.init_from_config(__config)
    content = _content_init.init_from_config(__config)
    result = PYPIPackage(config=__config, paths=paths, content=content)
    return __postinit_pypipackage(result)


def __init_pypipackage_from_config_path(__config_path: str):
    config = _config_init.init_config(src_path=__config_path)
    return __init_pypipackage_from_config(config)


def __init_pypipackage_from_paths(
    __package_path: str = None, __config_path: str = None
):
    if __package_path:
        result = PYPIPackage.init_from(__package_path)
    elif __config_path:
        result = __init_pypipackage_from_config_path(__config_path)
    else:
        print("unable to init pypi package")
        result = None
    return result


def __init_pypipackage_from_systemargs(__systemargs: dict[str, dict] = None):
    if "config_path" in __systemargs:
        path = __systemargs["config_path"]
        if isinstance(path, dict):
            path = path["value"]
        result = __init_pypipackage_from_paths(None, path)
    elif "package_path" in __systemargs:
        path = __systemargs["package_path"]
        if isinstance(path, dict):
            path = path["value"]
        result = __init_pypipackage_from_paths(path, None)
    else:
        result = None
    return result


def __init_pypipackage(
    package_path: str = None,
    config_path: str = None,
    system_args: dict[str, dict] = None,
):
    if package_path or config_path:
        result = __init_pypipackage_from_paths(package_path, config_path)
    elif system_args:
        result = __init_pypipackage_from_systemargs(system_args)
    else:
        result = None
    return result


def init_pypipackage(
    package_path: str = None,
    config_path: str = None,
    system_args: dict[str, dict] = None,
):
    return __init_pypipackage(
        package_path=package_path, config_path=config_path, system_args=system_args
    )


def init_config_str_method(__package: PYPIPackage):
    return _config_init.init_config_str_method(__package.config)
