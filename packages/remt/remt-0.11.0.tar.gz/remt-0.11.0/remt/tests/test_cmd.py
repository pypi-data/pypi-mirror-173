#
# remt - note-taking support tool for reMarkable tablet
#
# Copyright (C) 2018-2021 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Command line commands unit tests.
"""

import os.path
import typing as tp
from datetime import datetime

from remt import cmd as rcmd
from remt import meta as rmeta
from remt.error import ConfigError

import pytest
from unittest import mock

def test_ls_line() -> None:
    """
    Test creating `ls` command basic output line.
    """
    meta = tp.cast(rmeta.Meta, {'uuid': 'xyz'})
    result = rcmd.ls_line('a/b', meta)
    assert result == 'a/b'

@mock.patch.object(rcmd, 'datetime')
def test_ls_line_long(mock_dt: mock.MagicMock) -> None:
    """
    Test creating `ls` command long output line.
    """
    meta = {
        'pinned': True,
        'bookmarked': True,
        'type': 'CollectionType',
        'lastModified': '1526115458925',
    }
    mock_dt.fromtimestamp.return_value = datetime(2018, 5, 12, 9, 57, 38)
    result = rcmd.ls_line_long('a/b', tp.cast(rmeta.Meta, meta))
    assert result == 'db 2018-05-12 09:57:38 a/b'

def test_ls_filter_path() -> None:
    """
    Test `ls` command metadata filtering with parent path.
    """
    meta = tp.cast(
        dict[str, rmeta.Meta],
        {
            'a': {'uuid': 'xyz-a'},
            'a/b': {'uuid': 'xyz-ab'},
            'a/c': {'uuid': 'xyz-ac'},
            'b': {'uuid': 'xyz-b'},
            'c': {'uuid': 'xyz-c'}
        }
    )
    result = rcmd.ls_filter_path(meta, 'a')
    expected = tp.cast(
        dict[str, rmeta.Meta],
        {
            'a/b': {'uuid': 'xyz-ab'},
            'a/c': {'uuid': 'xyz-ac'},
        }
    )
    assert result == expected

def test_ls_filter_parent_uuid() -> None:
    """
    Test `ls` command metadata filtering for items with parent identified
    by UUID.
    """
    meta = tp.cast(
        dict[str, rmeta.Meta],
        {
            'a': {'uuid': 'uuid-1'},
            'a/b': {'uuid': 'uuid-2', 'parent': 'uuid-1'},
            'a/c': {'uuid': 'uuid-3', 'parent': 'uuid-1'},
            'd': {'uuid': 'uuid-4'},
        }
    )
    result = rcmd.ls_filter_parent_uuid(meta, 'uuid-1')
    expected = tp.cast(
        dict[str, rmeta.Meta],
        {
            'a/b': {'uuid': 'uuid-2', 'parent': 'uuid-1'},
            'a/c': {'uuid': 'uuid-3', 'parent': 'uuid-1'},
        }
    )
    assert result == expected

def test_ls_filter_parent_uuid_null() -> None:
    """
    Test `ls` command metadata filtering for items with parent identified
    by UUID when UUID is null.
    """
    meta = tp.cast(
        dict[str, rmeta.Meta],
        {
            'a': {'uuid': 'uuid-1'},
            'a/b': {'uuid': 'uuid-2', 'parent': 'uuid-1'},
            'a/c': {'uuid': 'uuid-3', 'parent': 'uuid-1'},
            'd': {'uuid': 'uuid-4'},
        }
    )
    result = rcmd.ls_filter_parent_uuid(meta, None)

    # only items with no parents expected
    expected = tp.cast(
        dict[str, rmeta.Meta],
        {
            'a': {'uuid': 'uuid-1'},
            'd': {'uuid': 'uuid-4'},
        }
    )
    assert expected == result

def test_read_config_error() -> None:
    """
    Test if error is raised when no Remt configuration project is found.
    """
    with mock.patch.object(os.path, 'exists') as exists:
        exists.return_value = False

        with pytest.raises(ConfigError):
            rcmd.read_config()

def test_norm_path() -> None:
    """
    Test path normalisation.
    """
    result = rcmd.norm_path('a//b/c//d///')
    assert 'a/b/c/d' == result

def test_norm_path_leading_slashes() -> None:
    """
    Test path normalisation with leading slashes.
    """
    result = rcmd.norm_path('///a//b/c//d///')
    assert 'a/b/c/d' == result

# vim: sw=4:et:ai
