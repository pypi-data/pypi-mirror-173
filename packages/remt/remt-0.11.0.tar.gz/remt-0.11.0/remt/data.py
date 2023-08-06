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
Data classes representing reMarkable tablet information.
"""

from __future__ import annotations

import cairo
import dataclasses as dtc
import enum
import operator
import typing as tp
from functools import total_ordering

# pen width used by reMarkable tablet tools
PEN_WIDTH_UKNOWN = 1
PEN_WIDTH_ERASE_AREA = 1
PEN_WIDTH_HIGHLIGHTER = 30

TEXT_SELECTION_ORDER = operator.attrgetter('y', 'x1', 'x2')

BrushPatterns: tp.TypeAlias = dict[str, cairo.SurfacePattern]

_ERRORS: set[str] = set()

@enum.unique
class Pen(enum.IntEnum):
    """
    Stroke pen id representing reMarkable tablet tools.

    Tool examples: ballpoint, fineliner, highlighter or eraser.
    """
    BALLPOINT_1 = 2
    BALLPOINT_2 = 15
    CALIGRAPHY = 21
    ERASER = 6
    ERASER_AREA = 8
    FINELINER_1 = 4
    FINELINER_2 = 17
    HIGHLIGHTER_1 = 5
    HIGHLIGHTER_2 = 18
    MARKER_1 = 3
    MARKER_2 = 16
    MECHANICAL_PENCIL_1 = 7
    MECHANICAL_PENCIL_2 = 13
    PAINTBRUSH_1 = 0
    PAINTBRUSH_2 = 12
    PENCIL_1 = 1
    PENCIL_2 = 14

    @classmethod
    def is_highlighter(cls, value: int) -> bool:
        return value in (cls.HIGHLIGHTER_1, cls.HIGHLIGHTER_2)

@enum.unique
class ColorIndex(enum.IntEnum):
    """
    Color index value.
    """
    BLACK = 0
    GRAY = 1
    WHITE = 2

    YELLOW = 3
    GREEN = 4
    PINK = 5

    BLUE = 6
    RED = 7

    GRAY_OVERLAP = 8

    @classmethod
    def _missing_(cls, value: tp.Any) -> ColorIndex:
        _ERRORS.add('Unknown color index: {}'.format(value))
        return ColorIndex.BLACK

class Color(tp.NamedTuple):
    red: float
    green: float
    blue: float
    alpha: float

class Style(tp.NamedTuple):
    tool_line: tp.Callable[..., tp.Any]
    color: Color
    join: cairo.LineJoin
    cap: cairo.LineCap
    dash: tp.List[int] = []
    brush: tp.Optional[BrushPatterns] = None

class Page(tp.NamedTuple):
    number: int

class PageEnd(tp.NamedTuple):
    number: int

class Layer(tp.NamedTuple):
    number: int

class Stroke(tp.NamedTuple):
    number: int
    pen: Pen
    color: ColorIndex
    width: float
    segments: tp.List['Segment']
    text: tp.Optional[str] = None

class Segment(tp.NamedTuple):
    number: int
    x: float
    y: float
    speed: float
    direction: float
    width: float
    pressure: float

DocumentItem = tp.Union[Page, PageEnd, Layer, Stroke, Segment]
Items = tp.Iterable[DocumentItem]

class Context(tp.NamedTuple):
    """
    Remt drawing context.
    """
    cr_surface: cairo.PDFSurface
    cr_ctx: cairo.Context
    pdf_doc: tp.Any  # Poppler.Document
    style: tp.Dict[Pen, Style]
    page_number: tp.Iterator[int]

Point = tp.Tuple[float, float]
Points = tp.List[tp.Tuple[float, float]]

class LinePath(tp.NamedTuple):
    """
    Line calculated using stroke and segment data of reMarkable tablet.

    :var width: Width of line.
    :var pressure: Line pressure level.
    :var points: List of line points.
    """
    width: float
    pressure: int
    points: Points

@dtc.dataclass(frozen=True)
@total_ordering
class TextSelection:
    """
    Information required to select text in a document with a horizontal
    line.

    The text selection defines ordering, which is used to sort the
    selections and to determine if two text selections overlap.

    :var x1: Start of line (x-axis coordinate).
    :var x2: End of line (x-axis coordinate).
    :var y: Y-axis coordinate of the horizontal line.
    """
    x1: float
    x2: float
    y: float

    def merge(self, other: 'TextSelection') -> 'TextSelection':
        """
        Merge two text selection objects.
        """
        return TextSelection(
            min(self.x1, other.x1),
            max(self.x2, other.x2),
            (self.y + other.y) / 2,
        )

    def overlaps(self, other: 'TextSelection', tolerance: float) -> bool:
        """
        Check if two text selection objects overlap.

        NOTE: It is assumed that this object and the other objects are
        sorted.

        :param other: Other text selection object.
        :param tolerance: Vertical line tolerance.
        """
        return other.y - self.y <= tolerance and other.x1 <= self.x2

    def __lt__(self, other: 'TextSelection') -> bool:
        return TEXT_SELECTION_ORDER(self) < TEXT_SELECTION_ORDER(other)

    def __eq__(self, other: tp.Any) -> bool:
        return TEXT_SELECTION_ORDER(self) == TEXT_SELECTION_ORDER(other)

# vim: sw=4:et:ai
