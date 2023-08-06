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
Tests for reading and parsing reMarkable tablet metadata.
"""

import os.path
import typing as tp

from remt import meta as rmeta
from remt.error import FileError, ConnectionError

import pytest
from unittest import mock

def test_fn_path() -> None:
    """
    Test creating UUID based path from metadata.
    """
    meta = tp.cast(rmeta.Meta, {'uuid': 'xyz'})
    result = rmeta.fn_path(meta, base='/x/y', ext='.met')
    assert '/x/y/xyz.met' == result

def test_read_meta() -> None:
    """
    Test reading reMarkable tablet metadata.
    """
    dirmeta = 'dir'

    with mock.patch('glob.glob') as mock_glob, \
            mock.patch('json.load') as mock_json_load, \
            mock.patch('builtins.open') as mock_open:  # noqa: F841

        mock_glob.side_effect = [
            # let's make read_meta resistant to some filesystem
            # inconsistencies by introducing non-matching files
            [
                'f1.content', 'f2.content', 'f3.content', 'f4.content',
                'f5.content', 'f6.content', 'f7.content',
            ],
            [
                'f1.metadata', 'f2.metadata', 'f3.metadata', 'f4.metadata',
                'f5.metadata', 'f6.metadata', 'f7.metadata',
            ],
        ]
        mock_json_load.side_effect = [
            {'visibleName': 'f1', 'deleted': False},
            {'pages': 3},

            # deleted filename shall not be visible in the results
            {'visibleName': 'f2', 'deleted': True},
            {'pages': 4},

            {'visibleName': 'f3'},
            {'pages': 5},

            {'visibleName': 'f4', 'parent': 'f3'},
            {'pages': 6},

            # in trash, shall not be visible in the results
            {'visibleName': 'f5', 'deleted': False, 'parent': 'trash'},
            {'pages': 9},

            # there is no parent 'has-parent', so it should be ignored
            {'visibleName': 'f6', 'deleted': False, 'parent': 'has-parent'},
            {'pages': 1},

            {'visibleName': 'f7'},
            {'pages': 12},
        ]
        result = rmeta.read_meta(dirmeta)
        assert ['f1', 'f3', 'f3/f4', 'f7'] == list(result)
        assert {'pages': 3} == result['f1']['content']  # type: ignore
        assert {'pages': 5} == result['f3']['content']  # type: ignore
        assert {'pages': 6} == result['f3/f4']['content']  # type: ignore
        assert {'pages': 12} == result['f7']['content']  # type: ignore

def test_fn_metadata_error() -> None:
    """
    Test if error is raised if there is no metadata for a path.
    """
    meta = {'a/b/': tp.cast(rmeta.Meta, {'uuid': 'xyz'})}

    with pytest.raises(FileError):
        rmeta.fn_metadata(meta, 'x/y')

def test_is_meta() -> None:
    """
    Test if a filename is reMarkable tablet meta file.
    """
    assert rmeta.is_meta('x.content')
    assert rmeta.is_meta('x.metadata')
    assert not rmeta.is_meta('x.pdf')

def test_find_meta_update() -> None:
    """
    Test finding reMarkable tablet meta files, which need to be updated in
    local cache.
    """
    files_remote = {
        'a': 10.0,
        'b': 10.0,
        'c': 10.0,
        'x': 11.0,  # updated meta file
        'y': 11.0,
        'n': 10.0,  # new meta file
    }
    files_local = {
        'a': 10.0,
        'b': 10.0,
        'c': 10.0,
        'x': 9.0,
        'y': 12.0,
        'm': 9.0,
    }

    result = rmeta.find_meta_update(files_remote, files_local)
    expected = ['n', 'x']
    assert expected == list(sorted(result))

def test_find_meta_delete() -> None:
    """
    Test finding reMarkable tablet meta files, which need to be removed
    from local cache.
    """
    files_remote = {
        'c': 10.0,
    }
    files_local = {
        'a': 10.0,  # to be removed
        'b': 10.0,  # to be removed
        'c': 10.0,
    }

    result = rmeta.find_meta_delete(files_remote, files_local)
    expected = ['a', 'b']
    assert expected == list(sorted(result))

def test_cache_dir() -> None:
    """
    Test generating cache directory for reMarkable tablet metadata.
    """
    with mock.patch.object(rmeta, 'getmac') as mock_getmac_mod, \
            mock.patch.object(os.path, 'expanduser') as mock_expand:

        mock_getmac_mod.get_mac_address.return_value = 'a:b:c'
        mock_expand.return_value = '/home/t-user'
        result = rmeta.cache_dir('a-host')
        assert '/home/t-user/.cache/remt/a:b:c' == result

def test_cache_dir_no_mac() -> None:
    """
    Test if error is raised when no MAC address is returned when generating
    cache directory for reMarkable tablet metadata.
    """
    with mock.patch.object(rmeta, 'getmac') as mock_getmac_mod:
        mock_getmac_mod.get_mac_address.return_value = None
        with pytest.raises(ConnectionError):
            rmeta.cache_dir('a-host')

def test_ls_local() -> None:
    """
    Test listing files in local cache.
    """
    with mock.patch('glob.glob') as mock_glob, \
            mock.patch('os.stat') as mock_stat:

        def create_stat(ts: float) -> mock.MagicMock:
            s = mock.MagicMock()
            s.st_mtime = ts
            return s

        mock_stat.side_effect = [create_stat(v) for v in range(1, 5)]
        mock_glob.return_value = [
            'x/y/1.content',
            'x/y/1.metadata',
            'x/y/2.content',
            'x/y/2.metadata',
        ]

        result = rmeta.ls_local('a-dir')

        expected = {
            '1.content': 1,
            '1.metadata': 2,
            '2.content': 3,
            '2.metadata': 4,
        }
        assert expected == result

@pytest.mark.asyncio
async def test_ls_remote() -> None:
    """
    Test listing metadata files from reMarkable tablet directory.
    """
    def create_fn(ts: float) -> mock.MagicMock:
        fn = mock.MagicMock()
        fn.filename = '{}.metadata'.format(ts)
        fn.attrs.mtime = ts
        return fn

    sftp = mock.MagicMock()
    sftp.readdir = mock.AsyncMock()
    sftp.readdir.return_value = [create_fn(v) for v in range(1, 5)]

    result = await rmeta.ls_remote(sftp)
    expected = {
        '1.metadata': 1,
        '2.metadata': 2,
        '3.metadata': 3,
        '4.metadata': 4,
    }
    assert expected == result

# vim: sw=4:et:ai
