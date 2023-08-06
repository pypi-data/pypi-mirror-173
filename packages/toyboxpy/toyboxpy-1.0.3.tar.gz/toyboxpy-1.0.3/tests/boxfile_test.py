# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import pytest
import sys
import os

# -- We need to import from our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.boxfile import Boxfile       # noqa: E402


def test_constructor_old_format():
    boxfile = Boxfile(os.path.join('tests', 'data', 'boxfile_old'))
    urls = boxfile.urls()
    assert len(urls) == 1
    url = urls[0]
    assert url.as_string == 'github.com/DidierMalenfant/pdbase'
    assert boxfile.versionsForUrl(url) == '1'
    assert boxfile.maybeInstalledVersionForUrl(url) is None
    assert boxfile.maybeLuaImportFile() is None


def test_constructor_current_format():
    boxfile = Boxfile(os.path.join('tests', 'data', 'boxfile_current'))
    urls = boxfile.urls()
    assert len(urls) == 1
    url = urls[0]
    assert url.as_string == 'github.com/DidierMalenfant/pdbase'
    assert boxfile.versionsForUrl(url) == '1'
    assert boxfile.maybeInstalledVersionForUrl(url) == '1.2.3'
    assert boxfile.maybeLuaImportFile() == 'source/main.lua'


def test_constructor_incorrect_format():
    folder = os.path.join('tests', 'data', 'boxfile_future')

    with pytest.raises(SyntaxError) as e:
        Boxfile(folder)

    test = 'Incorrect format for Boxfile \'' + os.path.join(folder, 'Boxfile') + '\'.\nMaybe you need to upgrade toybox?'
    assert str(e.value) == test


def test_constructor_malformed_file():
    folder = os.path.join('tests', 'data', 'boxfile_invalid')

    with pytest.raises(SyntaxError) as e:
        Boxfile(folder)

    test = 'Malformed JSON in Boxfile \'' + os.path.join(folder, 'Boxfile') + '\'.\nExpecting \',\' delimiter: line 3 column 5 (char 40).'
    assert str(e.value) == test
