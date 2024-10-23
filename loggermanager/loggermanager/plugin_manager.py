import pkg_resources


def get_available_loggers():
    loggers = {}
    for entry_point in pkg_resources.iter_entry_points("loggermanager.providers"):
        loggers[entry_point.name] = entry_point.load()
    return loggers


def get_logger_provider(provider_name, **kwargs):
    loggers = get_available_loggers()
    if provider_name not in loggers:
        raise ImportError(
            f"The logger provider '{provider_name}' is not installed or registered. "
            f"Please install it using 'pip install loggermanager_{provider_name}'."
        )
    return loggers[provider_name](**kwargs)
