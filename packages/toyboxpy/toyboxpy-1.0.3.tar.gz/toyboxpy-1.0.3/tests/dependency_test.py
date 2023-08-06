# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import pytest
import sys
import os

# -- We need to import from our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.dependency import Dependency       # noqa: E402
from toybox.dependency import DependencyError  # noqa: E402
from toybox.version import Version             # noqa: E402
from toybox.url import Url                     # noqa: E402


class MockGit:
    """Mock of a Git class for the purpose of testing the Dependency class."""

    def __init__(self, tags, branches=[]):
        """Setup access to the git repo at url."""
        self.tags = tags
        self.branches = branches

    def listTags(self):
        return self.tags

    def listTagVersions(self):
        # -- In our case we can use the same data as long as all tags passed to MockGit are version tags.
        tag_versions = []
        for tag in self.listTags():
            tag_versions.append(Version(tag))

        return tag_versions

    def listBranches(self):
        return self.branches

    def isATag(self, name):
        return name in self.tags

    def isABranch(self, name):
        return name in self.branches

    def getLatestCommitHashForBranch(self, branch):
        return 'aaf867d2725ab51a770b036c219e1cfb676e79b7'


@pytest.fixture
def dependency_object():
    dependency = Dependency(Url('toyboxpy.io/DidierMalenfant/MyProject.py'))
    dependency.git = MockGit(['v1.0.0', 'v1.0.2', 'v2.0.0', 'v2.1.0', 'v3.0.0', 'v3.2.3'],
                             {'main': 'aaf867d2725ab51a770b036c219e1cfb676e79b7', 'develop': '10167a78efd194d4984c3e670bec38b8ccaf97eb'})
    return dependency


@pytest.mark.parametrize('version_string, expected_results', [
    ('develop', [Version('develop')]),
    ('>1.0 <3 <2.5', [Version('>1.0.0'), Version('<3.0.0'), Version('<2.5.0')]),
    ('/' + os.path.join('My', 'Local', 'Folder'), [Version('/' + os.path.join('My', 'Local', 'Folder'))]),
    (os.path.join('J:', 'My', 'Local', 'Folder'), [Version(os.path.join('J:', 'My', 'Local', 'Folder'))])
])


def test_addVersions(dependency_object, version_string, expected_results):  # noqa: E304
    dependency_object.addVersions(version_string)
    assert dependency_object.versions == expected_results


def test_addVersions_incorrect_values(dependency_object):
    with pytest.raises(SyntaxError):
        dependency_object.addVersions('>1 <=4.5 >4 <6')


@pytest.mark.parametrize('version_string, expected_result', [
    ('>v1.2.3', 'v3.2.3'),
    ('3', 'v3.2.3'),
    ('<2.0.0', 'v1.0.2'),
    ('1.0', 'v1.0.2'),
    ('>v1.0.0 <2.0.0', 'v1.0.2'),
    ('>v1.0.0 <=2.0.0', 'v2.0.0'),
    ('/' + os.path.join('My', 'Test', 'Folder'), '/' + os.path.join('My', 'Test', 'Folder')),
    (os.path.join('F:', 'My', 'Test', 'Folder'), os.path.join('F:', 'My', 'Test', 'Folder')),
    ('main', 'main')
])


def test_resolveVersion(dependency_object, version_string, expected_result):  # noqa: E304
    dependency_object.addVersions(version_string)
    print(dependency_object.resolveVersion())
    print(str(Version(expected_result)))
    assert dependency_object.resolveVersion().original_version == expected_result


def test_resolveVersion_no_versions_added(dependency_object):
    with pytest.raises(DependencyError):
        dependency_object.resolveVersion()


def test_addVersions_unresolvable(dependency_object):
    dependency_object.addVersions('test')
    with pytest.raises(DependencyError):
        dependency_object.resolveVersion()
