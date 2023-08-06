# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import shutil
import platform

from .git import Git
from .version import Version
from .url import Url
from .exceptions import DependencyError
from .utils import Utils


class Dependency:
    """A helper class for toybox dependencies."""

    def __init__(self, url: Url):
        """Create a dependency given a URL and a tag or branch."""

        self.url = url

        self.git = Git('https://' + self.url.as_string + '.git')

        self.versions = []
        self.last_version_installed = None
        self.box_file = None

    def __str__(self):
        string_version = self.url.as_string + '@'

        if len(self.versions) > 1:
            string_version += '('

        separator = ''
        for version in self.versions:
            string_version += separator
            if version.isLocal():
                string_version += 'local'
            else:
                string_version += version.original_version

            separator = ' '

        if len(self.versions) > 1:
            string_version += ')'

        return string_version

    def subFolder(self) -> str:
        return os.path.join(self.url.server, self.url.username, self.url.repo_name)

    def resolveVersion(self) -> Version:
        branch = None
        versions = None

        try:
            for version in self.versions:
                if version.isLocal():
                    return version
                elif version.isBranch():
                    if branch is not None:
                        raise DependencyError

                    if self.git.isABranch(version.original_version):
                        commit_hash = self.git.getLatestCommitHashForBranch(version.original_version)
                        if commit_hash is None:
                            raise DependencyError

                        branch = Version(version.original_version + '@' + commit_hash)
                else:
                    if branch is not None:
                        raise DependencyError

                    if versions is None:
                        versions = self.git.listTagVersions()

                    versions = version.includedVersionsIn(versions)

            if branch is not None:
                return branch
            elif versions is None:
                raise DependencyError
            else:
                if len(versions) > 0:
                    return versions[-1]
                else:
                    raise DependencyError
        except DependencyError:
            raise DependencyError('Can\'t resolve version with \'' + self.originalVersions() + '\' for \'' + self.url.as_string + '\'.')

    def replaceVersions(self, versions: str):
        self.versions = []
        self.addVersions(versions)

    def addVersions(self, versions: str):
        separated_versions = versions.split(' ')
        if len(separated_versions) > 3:
            raise SyntaxError('Malformed version string \'' + versions + '\'. Too many versions.')

        for version in separated_versions:
            if len(version) == 0:
                continue

            for version in Version.maybeRangeFromIncompleteNumericVersion(version):
                self.versions.append(Version(version))

    def isATag(self, name: str) -> bool:
        return self.git.isATag(name)

    def isABranch(self, name: str) -> bool:
        return self.git.isABranch(name)

    def originalVersions(self) -> str:
        versions: str = ''

        for version in self.versions:
            if len(versions) != 0:
                versions += ' '

            versions += version.original_version

        return versions

    def installIn(self, toyboxes_folder: str) -> Version:
        version_resolved = self.resolveVersion()

        if version_resolved is None:
            raise DependencyError('Can\'t resolve version with \'' + self.originalVersions() + '\' for \'' + self.url.as_string + '\'.')

        if self.last_version_installed is not None and self.last_version_installed.original_version == version_resolved.original_version:
            return

        folder = os.path.join(toyboxes_folder, self.subFolder())
        Utils.deleteFolder(folder)

        if version_resolved.isLocal():
            system_name = platform.system()
            if system_name == 'Darwin' or system_name == 'Linux':
                # -- On macOs and Linux we can use softlinks to point to a local version of a toybox.
                Utils.softlinkFromTo(version_resolved.original_version, folder)
            else:
                Utils.copyFromTo(version_resolved.original_version, folder)
        else:
            os.makedirs(folder, exist_ok=True)

            self.git.cloneIn(version_resolved.original_version, folder)

        dependency_git_folder = os.path.join(folder, '.git')
        Utils.deleteFolder(dependency_git_folder, force_delete=True)

        self.last_version_installed = version_resolved

        return version_resolved

    def deleteFolderIn(self, toyboxes_folder: str):
        Utils.deleteFolder(os.path.join(toyboxes_folder, self.subFolder()))
