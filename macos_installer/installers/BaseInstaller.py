class BaseInstaller:
    """ Base class for all *Installer types"""

    def __init__(self,
                 logger=None,
                 package_info=None):
        """
        Create a mew base class instance

        Args:
            logger (obj): Logger instance
            package_info (obj): PackageInfo for this installer
        """

        self.logger = logger
        self.package_info = package_info
        self.name = self.package_info.name
        self.state = self.package_info.state

    def install(self):
        """
        Install this package

        Returns:
            No return value
        """
        self.logger.error("install not implemented")

    def remove(self):
        """
        Remove this package

        Returns:
            No return value
        """
        self.logger.error("remove not implemented")
