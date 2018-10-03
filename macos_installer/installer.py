#!/uar/bin/env python3

from standard_logger import get_logger
logger_instance = get_logger(application_name="macos_installer", console=True)

from .PackageManager import PackageManager


def main(data=None, logger=None):
    """
    Standalone entry point

    Args:
        data list(dict): Data structure. See package_data.py or README for examples.

    Returns:
         No return value

    """
    if not logger:
        logger = logger_instance
    PackageManager.all_actions(data=data, logger=logger)
