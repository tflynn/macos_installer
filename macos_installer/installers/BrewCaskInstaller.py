from run_command import run_command
from .BaseInstaller import BaseInstaller


class BrewCaskInstaller(BaseInstaller):
    """ Installer for a Homebrew Caskpackage"""

    def __init__(self,
                 logger=None,
                 package_info=None):
        """
        Create a BrewInstaller Cask class instance

        Args:
            logger (obj): Logger instance
            package_info (obj): PackageInfo for this installer
        """
        super(BrewCaskInstaller, self).__init__(logger=logger, package_info=package_info)

    def install(self):
        """
        Install a Homebrew Cask package

        Returns:
            bool:

            True if installation occurred.
            
            False if package already installed or installation failed
            
        """

        if self.is_present():
            self.logger.info("BrewCaskInstaller.install {0} is already installed".format(self.package_info.name))
            return False
        else:
            self.logger.info("BrewCaskInstaller.installing {0}".format(self.package_info.name))
            results, errors, status = run_command(cmd=["brew", "cask", "install", self.package_info.name])
            if self.is_present:
                self.logger.info("BrewCaskInstaller.install {0} succeeded".format(self.package_info.name))
                return True
            else:
                if "Error" in results:
                    self.logger.error("BrewCaskInstaller.install {0} failed errors {1}".format(
                        self.package_info.name, results))
                else:
                    self.logger.warning("BrewCaskInstaller.install {0} failed".format(self.package_info.name))
                return False

    def remove(self):
        """
        Remove a Homebrew Cask package

        Returns:
            bool:
            True if removal succeeded
            False if package not installed or removal failed.
        """
        if self.is_present():
            run_command(cmd=["brew", "cask", "uninstall", self.package_info.name])
            if self.is_present():
                self.logger.warning("BrewCaskInstaller.remove {0} removal failed".format(self.package_info.name))
                return False
            else:
                self.logger.info("BrewCaskInstaller.remove {0} removal succeeded".format(self.package_info.name))
                return True
        else:
            self.logger.info("BrewCaskInstaller.remove {0} is not installed".format(self.package_info.name))
            return False

    def is_present(self):
        """
        Is package present

        Returns:
            bool:
            True if installed
            False Otherwise
        """

        results, errors, status = run_command(cmd=["brew", "cask", "list"])
        results = results.split("\n")
        if self.package_info.name in results:
            return True
        else:
            return False