from .packages_data import PACKAGES_DATA
from .PackageInfo import PackageInfo

from .installers.BrewInstaller import BrewInstaller
from .installers.BrewCaskInstaller import BrewCaskInstaller
from .installers.MASInstaller import MASInstaller


class PackageManager():
    """ Manager for all packages """

    packages_info = []
    installers = []

    @classmethod
    def load_all_data(cls, logger=None, data=None):
        """
        Load all packages defined in the data

        Args:
            data list(dict): Data structure. See package_data.py or README for examples.

        Returns:
             list(obj): A list of populated PackageInfo instances
        """

        packages_data = data if data else PACKAGES_DATA
        cls.packages_info = PackageInfo.load_all_data(data=packages_data, logger=logger)
        return cls.packages_info

    @classmethod
    def create_installers(cls, logger=None, packages_info=None):
        """
        Create an appropriate installer for each configured package

        Args:
            packages_info list(obj): A list of PackageInfo instances

        Returns:
            list(obj) List of configured *Installer instances
        """

        if not packages_info:
            packages_info = cls.packages_info

        for package_info in packages_info:

            # Don't try to use an invalid package spec
            if not package_info.valid:
                continue

            if package_info.package_type == 'brew':
                installer = BrewInstaller(logger=logger, package_info=package_info)
                cls.installers.append(installer)
            elif package_info.package_type == 'brewcask':
                installer = BrewCaskInstaller(logger=logger, package_info=package_info)
                cls.installers.append(installer)
            elif package_info.package_type == 'mas':
                installer = MASInstaller(logger=logger, package_info=package_info)
                cls.installers.append(installer)
            else:
                pass

        return cls.installers

    @classmethod
    def run_installers(cls, logger=None, installers=None ):
        """
        Run all the installer instances

        Args:
            installers list(obj):  List of configured *Installer instances

        Returns:
            No return value
        """

        if not installers:
            installers = cls.installers

        for installer in installers:
            if installer.state == "present":
                installer.install()
            elif installer.state == "absent":
                installer.remove()
            else:
                pass

    @classmethod
    def all_actions(cls, logger=None, data=None):
        """
        Execute all actions for all configured packages i.e. install or remove them.

        Args:
            data list(dict): Data structure. See package_data.py or README for examples.

        Returns:
            No return value

        """
        packages_info = cls.load_all_data(data=data, logger=logger)
        installers = cls.create_installers(packages_info=packages_info, logger=logger)
        cls.run_installers(installers=installers, logger=logger)
