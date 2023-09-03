# cell.py

# Copyright (C) 2023 Ahmad Rahima

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from enum import Enum
from gi.repository import GObject


# ATTENTION: PyGObject does not support enums!
# gotta convet to some GObject type later. or just int.
# TODO: Rewrite this whole thing!
# MINE=0010 (EMPTY=0000 implicitly) then it would (~MINE=1101)
# OPEN=0100 (CLOSED=0000 implicitly)
class MineSweeperCellType(Enum): # type: ignore
    INVALID = 0b0000
    MINE    = 0b0001
    EMPTY   = 0b0011
    OPEN    = 0b0101
    CLOSED  = 0b0001
    CHECKED = 0b1001


class MineSweeperCell(GObject.Object):
    """
    The cell represented by the grid.

    Each cell holds a type representing the state of the cell.
    """

    __gtype_name__ = 'MineSweeperCell'

    type =  GObject.Property(
        nick='Type',
        blurb="The type (state) of cell.",
        flags=GObject.ParamFlags.READWRITE,
        type=int,
        default=MineSweeperCellType.INVALID.value)

    @GObject.Property(
        nick='Type Character',
        blurb='The character representing the cell type',
        type=str,
        flags=GObject.ParamFlags.READWRITE)
    def type_char(self):
        if self.type & MineSweeperCellType.OPEN.value <= 1: # closed
            return ''
        if self.is_empty():
            return self.type >> 4
        if self.is_mine():
            return '💣'
        elif self.type & MineSweeperCellType.CHECKED.value > 1: # checked
            return '⚑'

        raise TypeError('Cell has non-valid type!')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fill_mine(self) -> None:
        self.type &= ~0 << 2
        self.type |= MineSweeperCellType.MINE.value

        self.notify('type_char')

    def fill_mines(self, n: int) -> None:
        # avoid the first 4 bits!
        self.type = self.type | (n << 4)
        self.notify('type_char')

    def open(self) -> None:
        self.type &= (0xff << 4) | 0x7
        self.type |= MineSweeperCellType.OPEN.value
        self.notify('type_char')

    def close(self) -> None:
        self.type = (~MineSweeperCellType.OPEN.value | 1) & (self.type & 0xf8)
        self.notify('type_char')

    def is_mine(self) -> bool:
        return self.type & 0x3 == 1

    def is_empty(self) -> bool:
        return self.type & MineSweeperCellType.EMPTY.value == MineSweeperCellType.EMPTY.value
