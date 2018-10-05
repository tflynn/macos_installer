#!/uar/bin/env python3

from standard_logger import get_logger
from macos_installer.PackageManager import PackageManager

def main(data=None, logger=None):
    """
    Standalone entry point

    Args:
        data list(dict): Data structure. See package_data.py or README for examples.

    Returns:
         No return value

    """

    logger_instance = get_logger(application_name="macos_installer", console=True)
    if not logger:
        logger = logger_instance
    PackageManager.all_actions(data=data, logger=logger)


if __name__ == "__main__":
    main()
