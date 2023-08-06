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
PDF annotation indexer unit tests.
"""

from .. import indexer as ridx
from ..data import ColorIndex, Page, Pen, Segment, Stroke, TextSelection

from unittest import mock

def test_page_text() -> None:
    """
    Test getting text for each page stroke.
    """
    page = mock.MagicMock()
    with mock.patch.object(ridx, 'pdf_text') as mock_pdf_text:
        mock_pdf_text.side_effect = ['a', '', 'b', 'c']

        # note: number of strokes the same as number of above side effects
        ts = [TextSelection(i, i, 0) for i in range(1, 5)]
        result = ridx.page_text(page, ts)

        # empty strings are removed
        assert ['a', 'b', 'c'] == result

def test_fmt_header() -> None:
    """
    Test formatting page header in reStructuredText format.
    """
    page = mock.MagicMock()
    page.get_label.return_value = 'IX'
    page.get_index.return_value = '10'

    result = ridx.fmt_header(page)
    print(result)
    assert 'Page IX (10)\n============' == result

def test_fmt_text() -> None:
    """
    Test formatting a collection of texts in reStructuredText format.
    """
    # note: no need to test for empty strings as these are removed by
    # page_text function
    texts = ['abc', 'xyz\nzyx']
    result = ridx.fmt_text(texts)
    expected = """\
::

    abc
    xyz
    zyx
"""
    assert expected == result

def test_is_highlighter() -> None:
    """
    Check if an object is a reMarkable tablet stroke and is a highlighter.
    """
    assert not ridx.is_highlighter(Page(1))
    assert not ridx.is_highlighter(Stroke(1, Pen.FINELINER_1, ColorIndex(1), 2, []))
    assert ridx.is_highlighter(Stroke(1, Pen.HIGHLIGHTER_1, ColorIndex(1), 2, []))

def test_is_horizontal_line() -> None:
    """
    Test checking if a candidate is a horizontal line.
    """
    assert not ridx.is_horizontal_line(1, 10, 5, 3)
    assert ridx.is_horizontal_line(1, 10, 5, 10)

def test_to_line_selection() -> None:
    """
    Test converting reMarkable tablet stroke information to text selection
    data.
    """
    stroke = Stroke(
        1, Pen.HIGHLIGHTER_1, ColorIndex(1), 2,
        [
            create_segment(10, 10),
            create_segment(100, 15),
            create_segment(200, 20),
        ]
    )

    result = ridx.to_line_selection(stroke)

    assert result is not None
    assert 10 == result.x1
    assert 200 == result.x2
    assert 15 == result.y

def test_to_line_selection_none() -> None:
    """
    Test converting reMarkable tablet stroke information to null instead of
    text selection data.
    """
    stroke = Stroke(
        1, Pen.HIGHLIGHTER_1, ColorIndex(1), 2,
        [
            create_segment(10, 0),
            create_segment(100, 40),
            create_segment(200, 15),
        ]
    )
    result = ridx.to_line_selection(stroke)
    assert result is None

def create_segment(x: float, y: float) -> Segment:
    return Segment(1, x, y, 0, 0, 30, 1)

# vim: sw=4:et:ai
