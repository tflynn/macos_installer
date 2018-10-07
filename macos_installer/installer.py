#!/uar/bin/env python3

from standard_logger import get_logger
from macos_installer.PackageManager import PackageManager


def main(data=None, logger=None):
    """
    Standalone entry point for installation package

    Args:
        data (list(dict)): Data structure. See package_data.py or README for examples.
        logger (obj): logger instance
    
    Returns:
        Nothing returned
    """

    if not logger:
        logger = get_logger(application_name="macos_installer", console=True)
    PackageManager.all_actions(data=data, logger=logger)
    return


if __name__ == "__main__":
    main()
