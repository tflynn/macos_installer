#!/uar/bin/env python3

import os
import json

import traceback

from standard_logger import get_logger
logger = get_logger(application_name="macos_installer", console=True)

from run_command import run_command

from packages_data import PACKAGES_DATA


class PackageInfo:

    all_instances = None

    def __init__(self,
            full_name=None,
            name=None,
            package_type=None,
            mas_id=None,
            state=None):

        self.logger = logger
        self.valid = False
        self.full_name = full_name
        self.name = name
        self.package_type = package_type
        self.mas_id = mas_id
        self.state = state if state else "present"

    def set_field(self, name, value):
        self.__dict__[name] = value

    def __repr__(self):
        out = ""
        for key, value in self.__dict__.items():
            if key == "logger":
                continue
            sep = ',' if out else ''
            out = out + "{0}{1}:{2}".format(sep, key, value)

        return out

    def is_valid(self):
        # Mac Apple Store (mas) packages
        if self.package_type == 'mas' and not self.mas_id:
            logger.error("Package type 'mas' without 'mas_id'")
            return False
        else:
            return True

        # Homebrew
        if self.package_type == 'brew':
            return True if self.name else False

        # Homebrew Cash
        if self.package_type == 'brewcask':
            return True if self.name else False

        # package_type: zip, pkg, dmg or ? requires package_url
        return False

    def load_from_data(self, data):
        for field_name in self.__dict__.keys():
            if field_name in data:
                self.__dict__[field_name] = data[field_name]
        self.valid = self.is_valid()
        return self.valid

    @classmethod
    def load_all_data(cls, data = None):
        packages_info = []
        if not data:
            data = PACKAGES_DATA
        try:
            packages_data = json.loads(data)

            for package_data in  packages_data:
                package_info = PackageInfo()
                package_info.load_from_data(package_data)
                if package_info.is_valid():
                    packages_info.append(package_info)
                else:
                    logger.error("load_data: invalid data {0}".format(package_data))

            cls.all_instances = packages_info
            return cls.get_instances()
        except Exception as e:
            logger.error("load_data failed: {0} \n {1}".format(e, traceback.format_exc()))
            return None

    @classmethod
    def get_instances(cls):
        return cls.all_instances


class BaseInstaller:

    def __init__(self,
                 full_name=None,
                 name=None,
                 state=None):

        self.logger = logger
        self.full_name = full_name
        self.name = name
        self.state = state

    def install(self):
        logger.error("install not implemented")

    def remove(self):
        logger.error("remove not implemented")


class BrewInstaller(BaseInstaller):

    def __init__(self,
                 full_name=None,
                 name=None,
                 state=None):

        super(BrewInstaller, self).__init__(
            full_name=full_name,
            name=name,
            state=state
        )

    def install(self):
        if self.is_present():
            logger.info("BrewInstaller.install {0} is already installed".format(self.name))
        else:
            run_command(cmd=["brew", "install", self.name])
            if self.is_present:
                logger.info("BrewInstaller.install {0} succeeded".format(self.name))
            else:
                logger.warning("BrewInstaller.install {0} failed".format(self.name))

    def remove(self):
        if self.is_present():
            run_command(cmd=["brew", "uninstall", self.name])
            if self.is_present():
                logger.warning("BrewInstaller.remove {0} removal failed".format(self.name))
            else:
                logger.info("BrewInstaller.remove {0} removal succeeded".format(self.name))
        else:
            logger.info("BrewInstaller.remove {0} is not installed".format(self.name))

    def is_present(self):
        results, ignore = run_command(cmd=["brew","list"])
        results = results.split("\n")
        if self.name in results:
            return True
        else:
            return False


class BrewCaskInstaller(BaseInstaller):

    def __init__(self,
                 full_name=None,
                 name=None,
                 state=None):

        super(BrewCaskInstaller, self).__init__(
            full_name=full_name,
            name=name,
            state=state
        )

    def install(self):
        if self.is_present():
            logger.info("BrewCaskInstaller.install {0} is already installed".format(self.name))
        else:
            run_command(cmd=["brew", "cask", "install", self.name])
            if self.is_present:
                logger.info("BrewCaskInstaller.install {0} succeeded".format(self.name))
            else:
                logger.warning("BrewCaskInstaller.install {0} failed".format(self.name))

    def remove(self):
        if self.is_present():
            run_command(cmd=["brew", "cask", "uninstall", self.name])
            if self.is_present():
                logger.warning("BrewCaskInstaller.remove {0} removal failed".format(self.name))
            else:
                logger.info("BrewCaskInstaller.remove {0} removal succeeded".format(self.name))
        else:
            logger.info("BrewCaskInstaller.remove {0} is not installed".format(self.name))

    def is_present(self):
        results, ignore = run_command(cmd=["brew","cask", "list"])
        results = results.split("\n")
        if self.name in results:
            return True
        else:
            return False


class MASInstaller(BaseInstaller):

    def __init__(self,
                 full_name=None,
                 name=None,
                 state=None,
                 mas_id=None):

        super(MASInstaller, self).__init__(
            full_name=full_name,
            name=name,
            state=state
        )

        self.mas_id = mas_id

    def install(self):
        if self.is_present():
            logger.info("MASInstaller.install {0} is already installed".format(self.name))
        else:
            run_command(cmd=["mas", "install", self.mas_id])
            if self.is_present:
                logger.info("MASInstaller.install {0} succeeded".format(self.name))
            else:
                logger.warning("MASInstaller.install {0} failed".format(self.name))

    def remove(self):
        logger.warning("MASInstaller.remove ia experimental. Use at your own risk")
        if self.is_present():
            app_name = "/Applications/{0}.app".format(self.name)
            results, errors = run_command(cmd=["sudo","rm", "-rf", app_name])
            # logger.info("MASInstaller.remove results {0}".format(results))
            # logger.info("MASInstaller.remove errors {0}".format(errors))
            if self.is_present():
                logger.warning("MASInstaller.remove {0} removal failed".format(self.name))
            else:
                logger.info("MASInstaller.remove {0} removal succeeded".format(self.name))
            trash_dir = "{0}/.Trash/*".format(os.environ['HOME'])
            results, errors = run_command(cmd=["sudo", "rm", "-rf", trash_dir])
            # logger.info("MASInstaller.remove clear trash results {0}".format(results))
            # logger.info("MASInstaller.remove clear trash errors {0}".format(errors))
        else:
            logger.info("MASInstaller.remove {0} is not installed".format(self.name))

    def is_present(self):
        results, ignore = run_command(cmd=["mas","list"])
        results = results.split("\n")
        results = [result.split(" ")[0] for result in results]
        if self.mas_id in results:
            return True
        else:
            return False



class PackageManager():

    packages_info = []
    installers = []

    @classmethod
    def load_all_data(cls, data=None):
        packages_data = data if data else PACKAGES_DATA
        cls.packages_info = PackageInfo.load_all_data(packages_data)
        return cls.packages_info

    @classmethod
    def create_installers(cls, packages_info = None):

        if not packages_info:
            packages_info = cls.packages_info

        for package_info in packages_info:

            # Don't try to use an invalid package spec
            if not package_info.valid:
                continue

            full_name = package_info.full_name
            name = package_info.name
            state = package_info.state

            if package_info.package_type == 'brew':
                installer =  BrewInstaller(full_name=full_name, name=name, state=state)
                cls.installers.append(installer)
            elif package_info.package_type == 'brewcask':
                installer =  BrewCaskInstaller(full_name=full_name, name=name, state=state)
                cls.installers.append(installer)
            elif package_info.package_type == 'mas':
                installer =  MASInstaller(full_name=full_name, name=name, state=state, mas_id=package_info.mas_id)
                cls.installers.append(installer)
            else:
                pass

    @classmethod
    def run_installers(cls, installers=None ):

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
    def all_actions(cls, data=None):
        cls.load_all_data(data)
        cls.create_installers()
        cls.run_installers()


def main(data=None):
    PackageManager.all_actions(data)


if __name__ == "__main__":
    main()








