from typing import Iterable


def __get_fields(__cls) -> list[str]:
    result = []
    try:
        for field_key in ("__dataclass_fields__", "__fields__"):
            result = getattr(__cls, field_key, None)
            if result is not None:
                result = list(result.keys() if isinstance(result, dict) else result)
                break
    except BaseException:
        result = None
    return result


def __iter_field_identifier_pairs(__cls):
    prefix = str(__cls.__prefix__)
    for field_name in __get_fields(__cls):
        yield (prefix, field_name, field_name)
        for delimiter in ("_", "-", "."):
            yield (prefix, field_name, f"{prefix}{delimiter}{field_name}")


def __match_key(__key: str, __subconfig):
    result = None
    for (parent, name, comparator_name) in __iter_field_identifier_pairs(__subconfig):
        if __key == comparator_name:
            result = dict(parent=parent, key=name)
            break
    return result


def __postinit_varline(__varline: dict, __subconfigs):
    parent = __varline["parent"]
    if not parent:
        key = __varline["key"]
        for subconfig in __subconfigs:
            match = __match_key(key, subconfig)
            if match is not None:
                __varline.update(match)
                break
    return __varline


def postinit_varline(__varline: dict, __subconfigs: Iterable):
    return __postinit_varline(__varline, __subconfigs)
