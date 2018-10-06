import json
import traceback

from .packages_data import PACKAGES_DATA


class PackageInfo:
    """PackageInfo represents the data needed to install a single package"""

    all_instances = None

    def __init__(self,
            full_name=None,
            name=None,
            package_type=None,
            mas_id=None,
            state=None):
        """
        Create a new PackageInfo instance
        Args:
            full_name (str): Full package name e.g. "Atom Editor 1.31.1"
            name (str): Actual package name used for installation e.g. 'atom'
            package_type (str): Package type. One of 'brew', 'brewcask', 'mas'
            mas_id (str): Mac Apple Store id (Only required for Mac Apple Store package)
            state (str): 'present' or 'absent'
        """

        self.logger = None
        self.valid = False
        self.full_name = full_name
        self.name = name
        self.package_type = package_type
        self.mas_id = mas_id
        self.state = state if state else "present"
        self.force = "false"

    def set_field(self, name, value):
        """
        Set an internal field value by name

        Args:
            name (str): Field name
            value (obj): Field value (usually a string)

        Returns:
            No return value

        """
        self.__dict__[name] = value

    def __repr__(self):
        """
        Create the string representation of this object. For print(...) etc.

        Returns:
            String representation of this object

        """
        out = ""
        for key, value in self.__dict__.items():
            if key == "logger":
                continue
            sep = ',' if out else ''
            out = out + "{0}{1}:{2}".format(sep, key, value)

        return out

    def is_valid(self):
        """
        Are the settings for this instance valid and consistent?

        Returns:
            bool: True if valid, False otherwise
        """

        # Mac Apple Store (mas) packages
        if self.package_type == 'mas':
            if not self.mas_id:
                self.logger.error("Package type 'mas' without 'mas_id'")
                return False
            else:
                return True

        # Homebrew
        if self.package_type == 'brew':
            return True if self.name else False

        # Homebrew Cask
        if self.package_type == 'brewcask':
            return True if self.name else False

        # Homebrew Local Cask
        if self.package_type == 'brewcasklocal':
            return True if self.name else False

        # package_type: zip, pkg, dmg or ? requires package_url
        return False

    def load_from_data(self, data):
        """
        Load an instance from data structure.

        Args:
            data (dict): Data structure. See package_data.py or README for examples.

        Returns:
            bool: True if loaded object is valid, False otherwise
        """
        for field_name in self.__dict__.keys():
            if field_name in data:
                self.__dict__[field_name] = data[field_name]
        self.valid = self.is_valid()
        return self.valid

    @classmethod
    def load_all_data(cls, logger=None, data=None):
        """
        Load any number of instances from data.

        Args:
            data (dict): Data structure. See package_data.py or README for examples.

        Returns:
            list(obj):
            
            Success: list of populated PackageInfo instances
            
            Failure: None

        """

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
        """
        Get a list of all populated instances

        Returns:
            list(obj):
            A list of populated PackageInfo instances
        """
        return cls.all_instances
