import osiotk as _os
from ... import utils as _utils
from ...pypipackage import PYPIPackage
from json import loads as __init_kwargs_from_jsonsrc


def __kwargs_from_varlines(__varlines: list[dict]):
    results = {}
    for varline in (varline for varline in __varlines if isinstance(varline, dict)):
        parent = varline["parent"]
        if parent:
            if not parent in results:
                results[parent] = {}
            results[parent][varline["key"]] = varline["value"]
    return results


def __init_kwargs_from_rawsrc(__src: str):

    subconfigs = PYPIPackage.Config.__subconfigs__
    postinit_varline = _utils.build_varline_postinit(subconfigs)
    varlines = _utils.varlines_from_src(src=__src, postinit_varline=postinit_varline)
    kwargs = __kwargs_from_varlines(varlines)
    return kwargs


def __init_kwargs_from_src(__src: str):

    try:
        result = __init_kwargs_from_jsonsrc(__src)
        print("JSONSRC:", result)
    except BaseException:
        result = None
    if not result:
        try:
            result = __init_kwargs_from_rawsrc(__src)
        except BaseException:
            result = None
    return result


def __init_kwargs_from_path(__path: str, is_abspath: bool):
    if __path.endswith(".json"):
        result = _os.readjson(__path, is_abspath)
    else:
        src = _os.reads(__path, is_abspath=is_abspath)
        result = __init_kwargs_from_rawsrc(src)
    return result


def init_config_kwargs(__src: str = None, __path: str = None, is_abspath: bool = False):
    if __src:
        print("SRC EXISTS:", __src)
        result = __init_kwargs_from_src(__src)
    else:
        result = __init_kwargs_from_path(
            __path,
            is_abspath=is_abspath,
        )
    assert result is not None, __name__ + ".error: result is none"
    return result
