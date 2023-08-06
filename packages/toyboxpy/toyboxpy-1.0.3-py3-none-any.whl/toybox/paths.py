# SPDX-FileCopyrightText: 2022-present Paths.py Contributors
#
# SPDX-License-Identifier: MIT

import os

from .dependency import Dependency


class Paths:
    """Various paths used by toyboxpy."""

    @classmethod
    def boxfileFolder(cls) -> str:
        return os.getcwd()

    @classmethod
    def toyboxesFolder(cls) -> str:
        return os.path.join(Paths.boxfileFolder(), 'toyboxes')

    @classmethod
    def toyboxFolderFor(cls, dep: Dependency) -> str:
        return os.path.join(Paths.toyboxesFolder(), dep.subFolder())

    @classmethod
    def toyboxesBackupFolder(cls) -> str:
        return Paths.toyboxesFolder() + '.backup'

    @classmethod
    def toyboxBackupFolderFor(cls, dep: Dependency) -> str:
        return os.path.join(Paths.toyboxesBackupFolder(), dep.subFolder())

    @classmethod
    def assetsFolder(cls) -> str:
        return os.path.join(Paths.boxfileFolder(), 'source', 'toybox_assets')

    @classmethod
    def assetsFolderFor(cls, dep: Dependency, maybe_sub_folder: str = None) -> str:
        if maybe_sub_folder is None:
            maybe_sub_folder = dep.subFolder()
        return os.path.join(Paths.assetsFolder(), maybe_sub_folder)

    @classmethod
    def toyboxAssetsFolderFor(cls, dep: Dependency) -> str:
        return os.path.join(Paths.toyboxFolderFor(dep), 'assets')

    @classmethod
    def assetsBackupFolder(cls) -> str:
        return os.path.join(Paths.toyboxesFolder(), 'assets')

    @classmethod
    def assetsBackupFolderFor(cls, dep: Dependency, maybe_sub_folder: str = None) -> str:
        if maybe_sub_folder is None:
            maybe_sub_folder = dep.subFolder()
        return os.path.join(Paths.toyboxesFolder(), 'assets', maybe_sub_folder)

    @classmethod
    def preCommitFilePath(cls) -> str:
        return os.path.join('.git', 'hooks', 'pre-commit')

    @classmethod
    def preCommitFileBackupPath(cls) -> str:
        return Paths.preCommitFilePath() + '.toyboxes_backup'

    @classmethod
    def preCommitFileNoBackupPath(cls) -> str:
        return Paths.preCommitFilePath() + '.toyboxes_no_backup'
