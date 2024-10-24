import pkg_resources


def get_available_loggers():
    """
    Discover and load all available logger providers.

    This function scans for all entry points registered under the
    'loggermanager.providers' group, loads them, and returns a dictionary
    mapping provider names to their corresponding logger classes.

    Returns:
        dict: A dictionary where keys are provider names (str) and values are
              the loaded logger classes.

    Example:
        >>> loggers = get_available_loggers()
        >>> print(loggers)
        {
            'azure_appinsights': <class 'loggermanager_azure_appinsights.azure_appinsights_logger.AzureAppInsightsLogger'>,
            'aws_cloudwatch': <class 'loggermanager_aws_cloudwatch.aws_cloudwatch_logger.AWSCloudWatchLogger'>,
            'local_filesystem': <class 'loggermanager_local_filesystem.local_filesystem_logger.LocalFileSystemLogger'>
        }
    """
    loggers = {}
    for entry_point in pkg_resources.iter_entry_points("loggermanager.providers"):
        loggers[entry_point.name] = entry_point.load()
    return loggers


def get_logger_provider(provider_name, **kwargs):
    """
    Retrieve an instance of the specified logger provider.

    Args:
        provider_name (str): The name of the logger provider to retrieve.
                             This should match the name registered in the
                             entry points (e.g., 'azure_appinsights',
                             'aws_cloudwatch', 'local_filesystem').
        **kwargs: Arbitrary keyword arguments that will be passed to the
                  constructor of the logger class.

    Returns:
        LoggerInterface: An instance of the requested logger provider class,
                         initialized with the provided keyword arguments.

    Raises:
        ImportError: If the specified provider is not found among the
                     available loggers.

    Example:
        >>> logger = get_logger_provider('azure_appinsights', connection_string='Your_Connection_String')
        >>> logger.log_info("This is an info message.")

    Notes:
        - Ensure that the desired logger provider package (e.g.,
          'loggermanager_azure_appinsights') is installed in your environment.
        - The provider must be registered under the 'loggermanager.providers'
          entry point group.

    """
    loggers = get_available_loggers()
    if provider_name not in loggers:
        raise ImportError(
            f"The logger provider '{provider_name}' is not installed or registered. "
            f"Please install it using 'pip install loggermanager_{provider_name}'."
        )
    return loggers[provider_name](**kwargs)
