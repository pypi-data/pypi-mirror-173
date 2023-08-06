# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import getopt
import shutil

from pathlib import Path
from typing import List

from .__about__ import __version__
from .boxfile import Boxfile
from .exceptions import ArgumentError
from .version import Version
from .dependency import Dependency
from .git import Git
from .paths import Paths
from .utils import Utils
from .files import Files
from .url import Url


class Toybox:
    """A Lua, C and asset dependency manager for the Playdate SDK."""

    def __init__(self, args):
        """Initialise toybox based on user configuration."""

        self.box_file = None
        self.dependencies = []
        self.only_update = []
        self.installed_a_local_toybox = False

        try:
            # -- Gather the arguments
            opts, other_arguments = getopt.getopt(args, '')

            if len(other_arguments) == 0:
                raise SyntaxError('Expected a command! Maybe start with `toybox help`?')

            number_of_arguments = len(other_arguments)

            self.command = None
            self.argument = None
            self.second_argument = None

            i = 0
            argument = other_arguments[i]
            if len(argument):
                self.command = argument
            i += 1

            if i != number_of_arguments:
                argument = other_arguments[i]
                if len(argument):
                    self.argument = other_arguments[i]
                i += 1
                if i != number_of_arguments:
                    argument = other_arguments[i]
                    if len(argument):
                        self.second_argument = other_arguments[i]
                        i += 1

            if i != number_of_arguments:
                raise SyntaxError('Too many commands on command line.')

        except getopt.GetoptError:
            raise ArgumentError('Error reading arguments.')

    def main(self):
        switch = {
            'help': self.printUsage,
            'version': Toybox.printVersion,
            'license': Toybox.printLicense,
            'info': self.printInfo,
            'add': self.addDependency,
            'remove': self.removeDependency,
            'update': self.update,
            'check': self.checkForUpdates,
            'set': self.set,
        }

        if self.command is None:
            print('No command found.\n')
            Toybox.printUsage()
            return

        method = switch.get(self.command)
        if method is None:
            raise ArgumentError('Unknow command \'' + self.command + '\'.')

        method()

        Toybox.checkForToyboxPyUpdates()

    def printUsage(self):
        method = None

        if self.argument is not None:
            switch = {
                'topics': Toybox.printTopics,
                'set': Toybox.printSetUsage
            }

            method = switch.get(self.argument)
            if method is None:
                raise ArgumentError('Error: Unknown topic \'' + self.argument + '\'.')

        Toybox.printVersion()
        print('Usage:')

        if method is not None:
            method()
            return

        print('    toybox help                 - Show a help message.')
        print('    toybox help <topic>         - Show a help message on a topic (use \'help topics\' for a list).')
        print('    toybox version              - Get the Toybox version.')
        print('    toybox license              - Show the license for the app.')
        print('    toybox info                 - Describe your dependency set.')
        print('    toybox add <url>            - Add a new dependency.')
        print('    toybox add <url> <version>  - Add a new dependency with a specific version.')
        print('    toybox remove <url>         - Remove a dependency.')
        print('    toybox update               - Update all the dependencies.')
        print('    toybox update <dependency>  - Update a single dependency.')
        print('    toybox check                - Check for updates.')
        print('    toybox set <name> <value>   - Set a configuration value for this toybox.')

    def printInfo(self, folder: str = None, already_displayed: List['Url'] = []):
        if folder is None:
            print('Resolving dependencies...')
            self.box_file = box_file_for_folder = Boxfile(Paths.boxfileFolder())
        else:
            box_file_for_folder = Boxfile(folder)

        dependencies = box_file_for_folder.dependencies()
        if len(dependencies) == 0 and self.box_file == box_file_for_folder:
            print('Boxfile is empty.')
            return

        for dep in dependencies:
            if dep.url in already_displayed:
                continue

            already_displayed.append(dep.url)

            info_string = '       - ' + str(dep) + ' -> '

            dep_folder = Paths.toyboxFolderFor(dep)
            dep_folder_exists = os.path.exists(dep_folder)

            version_installed: str = self.box_file.maybeInstalledVersionForUrl(dep.url)
            if dep_folder_exists and version_installed:
                info_string += version_installed
            elif dep_folder_exists:
                info_string += 'Unknown version.'
            else:
                info_string += 'Not installed.'

            print(info_string)

            if dep_folder_exists:
                self.printInfo(dep_folder, already_displayed)

    def checkForUpdates(self, folder: str = None, already_displayed: List['Url'] = []) -> bool:
        if folder is None:
            print('Resolving dependencies...')
            self.box_file = box_file_for_folder = Boxfile(Paths.boxfileFolder())
        else:
            box_file_for_folder = Boxfile(folder)

        dependencies = box_file_for_folder.dependencies()
        if len(dependencies) == 0 and self.box_file == box_file_for_folder:
            print('Boxfile is empty.')
            return

        something_needs_updating = False

        for dep in dependencies:
            if dep.url in already_displayed:
                continue

            already_displayed.append(dep.url)

            version_available = dep.resolveVersion()
            if version_available is None:
                continue

            dep_folder = Paths.toyboxFolderFor(dep)
            if os.path.exists(dep_folder) is False:
                print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')
                something_needs_updating = True
                continue

            version_installed: str = self.box_file.maybeInstalledVersionForUrl(dep.url)
            if version_installed is None:
                print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')
                something_needs_updating = True
            else:
                if Version(version_installed) != version_available:
                    if version_available.isLocal():
                        print('       - ' + str(dep) + ' -> Local version not installed.')
                    elif version_available.isBranch():
                        print('       - ' + str(dep) + ' -> A more recent commit is available.')
                    else:
                        print('       - ' + str(dep) + ' -> Version ' + str(version_available) + ' is available.')

                    something_needs_updating = True

            something_needs_updating |= self.checkForUpdates(dep_folder, already_displayed)

        if folder is None and something_needs_updating is False:
            print('You\'re all up to date!!')

        return something_needs_updating

    def addDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'add\' command.')

        url = Url(self.argument)
        versions: str = self.second_argument

        new_dependency = Dependency(url)

        if versions is None:
            versions = new_dependency.git.getHeadBranch()

        new_dependency.replaceVersions(versions)

        versions = new_dependency.originalVersions()

        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.addDependencyWithURLAndVersions(url, versions)
        self.box_file.saveIfModified()

        print('Added a dependency for \'' + self.argument + '\' at \'' + versions + '\'.')

    def removeDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'remove\' command.')

        url = Url(self.argument)

        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.removeDependencyWithURL(url)
        self.box_file.saveIfModified()

        dep = Dependency(url)
        dep.deleteFolderIn(Paths.toyboxesFolder())

        print('Removed a dependency for \'' + self.argument + '\'.')

    def set(self):
        if self.argument is None:
            raise ArgumentError('Expected a name argument to \'set\' command.')

        switch = {
            'lua_import': self.setLuaImport,
            'assets_sub_folder': self.setAssetsSubFolder,
        }

        if self.argument is None:
            raise ArgumentError('Expected a value to set for \'' + self.argument + '\'.')

        method = switch.get(self.argument)
        if method is None:
            raise ArgumentError('Unknown value \'' + self.argument + '\' for set command.')

        method()

    def setLuaImport(self):
        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.setLuaImport(self.second_argument)
        self.box_file.saveIfModified()

        print('Set Lua import file to \'' + self.second_argument + '\'.')

    def setAssetsSubFolder(self):
        self.box_file = Boxfile(Paths.boxfileFolder())
        self.box_file.setAssetsSubFolder(self.second_argument)
        self.box_file.saveIfModified()

        print('Set assets sub folder path to \'' + self.second_argument + '\'.')

    def installDependency(self, dep: Dependency, no_copying: bool = False):
        dependency_is_new = True

        for other_dep in self.dependencies:
            if other_dep.url == dep.url:
                other_dep.versions += dep.versions
                dep = other_dep
                dependency_is_new = False

        should_copy = len(self.only_update) != 0 and dep.url.repo_name not in self.only_update and Toybox.toyboxExistsInBackup(dep)

        if (no_copying is False) and should_copy:
            self.copyToyboxFromBackup(dep)
            self.copyAssetsFromBackupIfAny(dep)
        else:
            version = dep.installIn(Paths.toyboxesFolder())
            if version is not None:
                installed_version: str = version.original_version

                if version.isBranch():
                    commit_hash = dep.git.getLatestCommitHashForBranch(version.original_version)
                    if commit_hash is None:
                        raise RuntimeError('Could not find latest commit hash for branch ' + version.original_version + '.')

                    installed_version += '@' + commit_hash
                elif version.isLocal():
                    self.installed_a_local_toybox = True

                info_string = 'Installed \'' + str(dep) + '\' -> ' + str(version)

                if should_copy and no_copying:
                    info_string += ' (force-installed by another dependency)'
                    self.only_update.append(dep.url.repo_name)

                print(info_string + '.')

                self.box_file.setInstalledVersionForDependency(dep, installed_version)

            no_copying = True

            self.moveAssetsFromToyboxIfAny(dep)

        dep_box_file = Boxfile.boxfileForDependency(dep)
        for child_dep in dep_box_file.dependencies():
            self.installDependency(child_dep, no_copying)

        if dependency_is_new:
            self.dependencies.append(dep)

    def update(self):
        if self.argument is not None:
            self.only_update.append(self.argument)

        Toybox.backupToyboxes()
        Toybox.backupAssets()

        try:
            self.box_file = Boxfile(Paths.boxfileFolder())
            for dep in self.box_file.dependencies():
                self.installDependency(dep)

            folder = Paths.toyboxesFolder()
            if os.path.exists(folder):
                Files.generateReadMeFileIn(folder)
                Files.generateLuaIncludeFile(self.dependencies)
                Files.generateMakefile(self.dependencies)
                Files.generateIncludeFile(self.dependencies)

            folder = Paths.assetsFolder()
            if os.path.exists(folder):
                Files.generateReadMeFileIn(folder)

            self.box_file.saveIfModified()

        except Exception:
            Toybox.restoreAssetsBackup()
            Toybox.restoreToyboxesBackup()
            raise

        Toybox.deleteToyboxesBackup()
        Toybox.deleteAssetsBackup()

        Files.restorePreCommitFileIfAny()

        if self.installed_a_local_toybox:
            Files.generatePreCommitFile()

        print('Finished.')

    @classmethod
    def printVersion(cls):
        if os.name == 'nt':
            # -- Windows Powershell doesn't support emoticons
            version_string = ''
        else:
            version_string = '🧸 '

        version_string += 'toybox.py v' + __version__
        print(version_string)

    @classmethod
    def printLicense(cls):
        Toybox.printVersion()
        print('MIT License')
        print('')
        print('Copyright (c) 2022-present toybox.py Contributors')
        print('')
        print('Permission is hereby granted, free of charge, to any person obtaining a copy')
        print('of this software and associated documentation files (the "Software"), to deal')
        print('in the Software without restriction, including without limitation the rights')
        print('to use, copy, modify, merge, publish, distribute, sublicense, and/or sell')
        print('copies of the Software, and to permit persons to whom the Software is')
        print('furnished to do so, subject to the following conditions:')
        print('')
        print('The above copyright notice and this permission notice shall be included in all')
        print('copies or substantial portions of the Software.')
        print('')
        print('THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR')
        print('IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,')
        print('FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE')
        print('AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER')
        print('LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,')
        print('OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE')
        print('SOFTWARE.')
        print('')
        print('Official repo can be found at https://github.com/toyboxpy/toybox.py')

    @classmethod
    def printSetUsage(cls):
        print('    toybox set lua_import <value>        - Set the lua filename to import.')
        print('    toybox set assets_sub_folder <value> - Set the subfolder to use for assets.')

    @classmethod
    def printTopics(cls):
        print('    set     - List the names accepted bu the set command.')

    @classmethod
    def backupToyboxes(cls):
        Utils.backup(Paths.toyboxesFolder(), Paths.toyboxesBackupFolder())

    @classmethod
    def restoreToyboxesBackup(cls):
        Utils.restore(Paths.toyboxesBackupFolder(), Paths.toyboxesFolder())

    @classmethod
    def backupAssets(cls):
        Utils.backup(Paths.assetsFolder(), Paths.assetsBackupFolder())

    @classmethod
    def restoreAssetsBackup(cls):
        Utils.restore(Paths.assetsBackupFolder(), Paths.assetsFolder())

    @classmethod
    def toyboxExistsInBackup(cls, dep: Dependency):
        return os.path.exists(Paths.toyboxBackupFolderFor(dep))

    @classmethod
    def copyToyboxFromBackup(cls, dep: Dependency):
        source_path = Paths.toyboxBackupFolderFor(dep)
        dest_path = Paths.toyboxFolderFor(dep)
        if not os.path.exists(source_path):
            raise RuntimeError('Backup from ' + dep.subFolder() + ' cannot be found.')

        if os.path.exists(dest_path):
            # -- We may have already copied this toybox from another dependency.
            Utils.deleteFolder(dest_path)

        shutil.copytree(source_path, dest_path)

    @classmethod
    def copyAssetsFromBackupIfAny(cls, dep: Dependency):
        maybe_config_asset_folder = Boxfile.boxfileForDependency(dep).maybeAssetsSubFolder()
        source_path = Paths.assetsBackupFolderFor(dep, maybe_config_asset_folder)
        if os.path.exists(source_path):
            shutil.copytree(source_path, Paths.assetsFolderFor(dep, maybe_config_asset_folder))

    @classmethod
    def deleteToyboxesBackup(cls):
        Utils.deleteFolder(Paths.toyboxesBackupFolder())

    @classmethod
    def deleteAssetsBackup(cls):
        Utils.deleteFolder(Paths.assetsBackupFolder())

    @classmethod
    def moveAssetsFromToyboxIfAny(cls, dep: Dependency):
        source_path = os.path.join(Paths.toyboxAssetsFolderFor(dep))
        if not os.path.exists(source_path):
            return

        maybe_config_asset_folder = Boxfile.boxfileForDependency(dep).maybeAssetsSubFolder()
        dest_path = Paths.assetsFolderFor(dep, maybe_config_asset_folder)
        if os.path.exists(dest_path):
            raise RuntimeError('Something already installed assets in \'' + dest_path + '\'')

        os.makedirs(Path(dest_path).parent, exist_ok=True)

        shutil.move(source_path, dest_path)

    @classmethod
    def checkForToyboxPyUpdates(cls):
        try:
            latest_version = Git('https://github.com/toyboxpy/toybox.py').getLatestVersion()
            if latest_version is None:
                return

            if latest_version > Version(__version__):
                print('‼️  Version v' + str(latest_version) + ' is available for toybox.py. You have v' + __version__ + ' ‼️')
                print('Please run \'pip install toyboxpy --upgrade\' to upgrade.')
        except Exception:
            pass
