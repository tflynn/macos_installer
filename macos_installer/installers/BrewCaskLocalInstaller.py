import sys
import os
from os import path
import glob
import shutil
import re

from run_command import run_command
from .BaseInstaller import BaseInstaller

STARTUP_DIR = "{0}/.startup".format(os.environ['HOME'])

LOCAL_CASK_REPO_NAME = "private_casks"
LOCAL_CASK_REPO_DIR = "{0}/{1}".format(STARTUP_DIR,LOCAL_CASK_REPO_NAME)
LOCAL_CASK_REPO_URL = "git@github.com:tflynn/{0}.git".format(LOCAL_CASK_REPO_NAME)


class BrewCaskLocalInstaller(BaseInstaller):
    """ Installer for a Homebrew CaskLocal package"""

    def __init__(self,
                 logger=None,
                 package_info=None):
        """
        Create a Homebrew CaskLocal Installer class instance

        Args:
            logger (obj): Logger instance
            package_info (obj): PackageInfo for this installer
        """
        super(BrewCaskLocalInstaller, self).__init__(logger=logger, package_info=package_info)

    def ensure_local_cask_repo_present(self):
        """
        Ensure that the repo contain the local cask definitions is present

        Returns:
            None
            Will exit if an error occurs during repo cloning.
        """
        if not path.exists(LOCAL_CASK_REPO_DIR):
            # Switch to appropriate directory
            start_dir = os.getcwd()
            os.chdir(STARTUP_DIR)
            # git clone git@github.com:tflynn/private_casks.git
            cmd = ['git', 'clone', LOCAL_CASK_REPO_URL]
            results, errors = run_command(cmd=cmd)
            os.chdir(start_dir)
            if re.search('error', results, re.IGNORECASE) or errors:
                self.logger.error("BrewCaskLocalInstaller error cloning cask definitions repo")
                sys.exit(1)

    def get_cask_info(self):
        """
        Extract some information from the cask definition

        Returns:
            Tuple(str)(cask name, directory containing cask, qualified cask name, application name)
            Will exit if application name cannot be determined

        """
        # TODO This needs improvement
        local_cask_name = self.package_info.name + ".rb"
        local_cask_dir = "{0}/casks".format(LOCAL_CASK_REPO_DIR)
        local_cask_qname_file = "{0}/{1}".format(local_cask_dir, local_cask_name)
        app_name = None
        with open(local_cask_qname_file, 'r') as cask_def:
            for cask_def_line in cask_def.readlines():
                cleaned_cask_def_line = cask_def_line.strip().replace("\n", '')
                # print('z' + cleaned_cask_def_line + 'z')
                if cleaned_cask_def_line.startswith('app'):
                    # print('x' + cleaned_cask_def_line[4:] + 'x')
                    app_name = cleaned_cask_def_line[4:].strip()[1:-1]
                    # print(app_name)

        if not app_name:
            self.logger.error("BrewCaskLocalInstaller can't determine application name from cask")
            sys.exit(1)

        return local_cask_name, local_cask_dir, local_cask_qname_file, app_name

    def process_receipt_info(self, app_name):
        """
        Process a receipts zip if present in the installed App

        Args:
            app_name: Name of app to search for receipts zip

        Returns:
            True: If no zip or no errors during unzip processing
            False: If any errors during unzip processing
        """
        tmp_dir = os.environ['MY_TEMP']

        # Extract receipts zip and unpack to /private/var/db/receipts
        possible_zips = glob.glob("/Applications/{0}/*-receipts.zip".format(app_name), recursive=False)
        if possible_zips:
            receipts_zip_file = possible_zips[0]
            full_target_dir = '/private/var/db/receipts'
            # "sudo unzip <zip file name> -d dir"
            cmd = ['sudo', 'unzip', receipts_zip_file, '-d', full_target_dir]
            results, errors = run_command(cmd=cmd)
            if re.search('error', results, re.IGNORECASE) or errors:
                if results:
                    self.logger.info("unzip receipts results {0}".format(results))
                if errors:
                    self.logger.info("unzip receipts errors {0}".format(errors))
                return False

        return True

    def install(self):
        """
        Install a Homebrew CaskLocal package

        Returns:
            True if installation occurred.
            False if package already installed or installation failed
        """
        self.ensure_local_cask_repo_present()

        if self.is_present():
            self.logger.info("BrewCaskLocalInstaller.install {0} is already installed".format(self.package_info.name))
            return False
        else:
            local_cask_name, local_cask_dir, local_cask_qname_file, app_name = self.get_cask_info()

            self.logger.info("BrewCaskLocalInstaller.installing {0}".format(self.package_info.name))

            start_dir = os.getcwd()
            os.chdir(local_cask_dir)
            results, errors = run_command(cmd=["brew", "cask", "install", local_cask_name])
            os.chdir(start_dir)

            if re.search('error', results, re.IGNORECASE) or errors:
                self.logger.error("BrewCaskLocalInstaller.install {0} failed {1} errors {2}".format(
                    self.package_info.name, results, errors))
                return False
            else:
                if self.is_present():
                    status = self.process_receipt_info(app_name)
                    if status:
                        self.logger.info("BrewCaskLocalInstaller.install {0} succeeded".format(self.package_info.name))
                        return True
                    else:
                        self.logger.error("BrewCaskLocalInstaller.install {0} failed".format(self.package_info.name))
                        return False

    def remove(self):
        """
        Remove a Homebrew CaskLocal package

        Returns:
            True if removal succeeded
            False if package not installed or removal failed.
        """
        self.ensure_local_cask_repo_present()

        if self.is_present():
            results, errors = run_command(cmd=["brew", "cask", "uninstall", self.package_info.name])
            if re.search('error', results, re.IGNORECASE) or errors:
                self.logger.error("BrewCaskLocalInstaller.remove {0} failed {1} errors {2}".format(
                    self.package_info.name, results, errors))
                return False
            if self.is_present():
                self.logger.warning("BrewCaskLocalInstaller.remove {0} removal failed".format(self.package_info.name))
                return False
            else:
                self.logger.info("BrewCaskLocalInstaller.remove {0} removal succeeded".format(self.package_info.name))
                return True
        else:
            self.logger.info("BrewCaskLocalInstaller.remove {0} is not installed".format(self.package_info.name))
            return False

    def is_present(self):
        """
        Is package present

        Returns:
            True if installed
            False Otherwise
        """
        # Check to see whether the app is present (and therefore installed) in /Applications
        local_cask_name, local_cask_dir, local_cask_qname_file, app_name = self.get_cask_info()
        app_exists = path.exists("/Applications/{0}".format(app_name))
        return app_exists
