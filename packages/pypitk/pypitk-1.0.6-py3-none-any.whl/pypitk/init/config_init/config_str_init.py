from ...pypipackage import PYPIPackage


def __iter_field_identifiers(__field_id: str, parent_id: str):
    return iter(
        [f"*{__field_id}*"]
        + [f"*{parent_id}{delim}{__field_id}*" for delim in ("-", "_", ".")]
    )


def __config_str_base(__config: PYPIPackage.Config, __str: str):
    result = str(__str)
    if "*" in result:
        subconfig_dicts = dict(
            package=__config.package.dict(),
            build=__config.build.dict(),
            content=__config.build.dict(),
        )
        for subconfig_id, subconfig_dict in subconfig_dicts.items():
            for key, value in subconfig_dict.items():
                formatted_value = str(value) if isinstance(value, bool) else value
                for field_id in __iter_field_identifiers(key, parent_id=subconfig_id):
                    result = result.replace(field_id, formatted_value)
    return result


def __config_str_method(__config: PYPIPackage.Config):
    def config_str(__str: str):
        return __config_str_base(__config, __str)

    return config_str


def init_config_str_method(__config: PYPIPackage.Config):
    return __config_str_method(__config)
