import os
from run_command import run_command
from .BaseInstaller import BaseInstaller


class MASInstaller(BaseInstaller):
    """ Installer for a MAS (Mac Apple Store) package"""

    def __init__(self,
                 logger=None,
                 package_info=None):
        """
        Create a BrewInstaller class instance

        Args:
            logger (obj): Logger instance
            package_info (obj): PackageInfo for this installer
        """
        super(MASInstaller, self).__init__(logger=logger, package_info=package_info)

    def install(self):
        """
        Install a MAS package

        Returns:
            bool:

            True if installation occurred.

            False if package already installed or installation failed

        """

        if self.is_present():
            self.logger.info("MASInstaller.install {0} is already installed".format(self.package_info.name))
            return False
        else:
            self.logger.info("MASInstaller.installing {0}".format(self.package_info.name))
            results, errors = run_command(cmd=["mas", "install", self.package_info.mas_id])
            if "Error:"in results or "Warning:" in results:
                self.logger.error("MASInstaller.install {0} failed {1}".format(self.package_info.name, results))
                return False
            if self.is_present:
                self.logger.info("MASInstaller.install {0} succeeded".format(self.package_info.name))
                return True
            else:
                self.logger.warning("MASInstaller.install {0} failed".format(self.package_info.name))
                return False

    def remove(self):
        """
        Remove a MAS package


        Returns:
            bool:

            True if removal succeeded

            False if package not installed or removal failed.

        """

        self.logger.warning("MASInstaller.remove ia experimental. Use at your own risk")
        if self.is_present():
            app_name = "/Applications/{0}.app".format(self.package_info.name)
            results, errors = run_command(cmd=["sudo","rm", "-rf", app_name])
            if "Error:"in results or "Warning:" in results:
                self.logger.error("MASInstaller.remove {0} failed {1}".format(self.package_info.name, results))
                return False
            if self.is_present():
                self.logger.warning("MASInstaller.remove {0} removal failed".format(self.package_info.name))
                return False
            else:
                self.logger.info("MASInstaller.remove {0} removal succeeded".format(self.package_info.name))

                trash_dir = "{0}/.Trash/*".format(os.environ['HOME'])
                run_command(cmd=["sudo", "rm", "-rf", trash_dir])
                #results, errors = run_command(cmd=["sudo", "rm", "-rf", trash_dir])
                # logger.info("MASInstaller.remove clear trash results {0}".format(results))
                # logger.info("MASInstaller.remove clear trash errors {0}".format(errors))
                return True
        else:
            self.logger.info("MASInstaller.remove {0} is not installed".format(self.package_info.name))
            return False

    def is_present(self):
        """
        Is package present

        Returns:
            bool:

            True if installed

            False Otherwise
            
        """

        results, ignore = run_command(cmd=["mas","list"])
        results = results.split("\n")
        results = [result.split(" ")[0] for result in results]
        if self.package_info.mas_id in results:
            return True
        else:
            return False
