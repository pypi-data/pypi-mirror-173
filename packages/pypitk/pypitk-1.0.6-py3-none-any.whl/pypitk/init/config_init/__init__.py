from . import subconfig_init as _subconfig_init
from ...pypipackage import PYPIPackage
from . import kwargs_init as _kwargs_init
from . import config_str_init as _config_str_init
from ...utils import util as _util


def init_config_from_kwargs(kwargs: dict = None):
    print(kwargs.keys())
    kwargs_ = {} if not kwargs else kwargs
    results = {}
    for subconfig_id in (
        subconfig.__prefix__ for subconfig in PYPIPackage.Config.__subconfigs__
    ):
        init_id = f"init_{subconfig_id}_subconfig"
        init = getattr(_subconfig_init, init_id)
        subconfig_kwargs = kwargs_[subconfig_id]
        subconfig = init(subconfig_kwargs)
        results[subconfig_id] = subconfig
    config = PYPIPackage.Config(**results)
    config.package.parentdir = _util.format_package_path(
        config.package.name, config.package.parentdir
    )
    return config


def init_config(src_path: str = None, pypitk_config: str = None):
    kwargs = _kwargs_init.init_config_kwargs(pypitk_config, src_path, is_abspath=True)
    config = init_config_from_kwargs(kwargs=kwargs)
    return config


def init_config_str_method(__config: PYPIPackage.Config):
    return _config_str_init.init_config_str_method(__config)
