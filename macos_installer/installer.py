#!/uar/bin/env python3

from standard_logger import get_logger
from macos_installer.PackageManager import PackageManager


def main(data=None, logger=None):
    """
    Standalone entry point for installation package

    :param data: list(dict): Data structure. See package_data.py or README for examples.
    :param logger: logger instance
    :return: No return
    """

    logger_instance = get_logger(application_name="macos_installer", console=True)
    if not logger:
        logger = logger_instance
    PackageManager.all_actions(data=data, logger=logger)
    return

if __name__ == "__main__":
    main()
