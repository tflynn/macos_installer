from run_command import run_command
from .BaseInstaller import BaseInstaller


class BrewInstaller(BaseInstaller):
    """ Installer for a Homebrew package"""

    def __init__(self,
                 logger=None,
                 package_info=None):
        """
        Create a BrewInstaller class instance

        Args:
            logger (obj): Logger instance
            package_info (obj): PackageInfo for this installer
        """
        super(BrewInstaller, self).__init__(logger=logger, package_info=package_info)

    def install(self):
        """
        Install a Homebrew package

        Returns:
            bool:

            True if installation occurred.

            False if package already installed or installation failed

        """

        if self.is_present():
            self.logger.info("BrewInstaller.install {0} is already installed".format(self.package_info.name))
            return False
        else:
            self.logger.info("BrewInstaller.installing {0}".format(self.package_info.name))
            cmd = ["brew", "install", self.package_info.name]
            results = run_command(cmd=cmd, logger=self.logger)
            if results.success:
                if self.is_present:
                    self.logger.info("BrewInstaller.install {0} succeeded".format(self.package_info.name))
                    return True
                else:
                    self.logger.warning("BrewInstaller.install {0} failed".format(self.package_info.name))
                    return False
            else:
                self.logger.error("BrewInstaller.install {0} failed status {1} results {2} errors {3}".format(
                    self.package_info.name, results.status_code, results.results, results.errors))
                return False

    def remove(self):
        """
        Remove a Homebrew package

        Returns:
            bool:

            True if removal succeeded

            False if package not installed or removal failed.

        """
        if self.is_present():
            cmd = ["brew", "uninstall", self.package_info.name]
            results = run_command(cmd=cmd, logger=self.logger)
            if results.success:
                if self.is_present():
                    self.logger.warning("BrewInstaller.remove {0} removal failed".format(self.package_info.name))
                    return False
                else:
                    self.logger.info("BrewInstaller.remove {0} removal succeeded".format(self.package_info.name))
                    return True
            else:
                self.logger.error("BrewInstaller.remove {0} failed status {1} results {2} errors {3}".format(
                    self.package_info.name, results.status_code, results.results, results.errors))
                return False
        else:
            self.logger.info("BrewInstaller.remove {0} is not installed".format(self.package_info.name))
            return False

    def is_present(self):
        """
        Is package present

        Returns:
            bool:

            True if installed

            False Otherwise
            
        """
        cmd = ["brew", "list"]
        results = run_command(cmd=cmd, logger=self.logger)
        if results.success:
            results = results.results.split("\n")
            if self.name in results:
                return True
            else:
                return False
        else:
            return False
