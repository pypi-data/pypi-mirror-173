from .subconfigs import postinit_varline as _postinit_varline
from .varlines import varline as varline


def __build_varline_postinit(__subconfigs):
    def postinit_varline(__varline: dict):
        return _postinit_varline(__varline, __subconfigs)

    return postinit_varline


def build_varline_postinit(__subconfigs):
    return __build_varline_postinit(__subconfigs)


def __varlines_from_src(src: str, postinit_varline):
    assert isinstance(src, str), __name__ + " src is not string"
    result = []
    for line in src.splitlines(keepends=False):
        _varline = varline(line, postinit_varline=postinit_varline)
        if _varline is not None:
            if _varline.get("is_varline", False):
                result.append(_varline)
    return result


def varlines_from_src(src: str, postinit_varline):
    return __varlines_from_src(src=src, postinit_varline=postinit_varline)
