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


from enum import IntEnum
from gi.repository import GObject


# ATTENTION: PyGObject does not support enums!
# gotta convet to some GObject type later. or just int.
class MineSweeperCellType(IntEnum): # type: ignore
    MINE = 0b0001
    OPEN = 0b0010
    CHECKED = 0b0100

    @property
    def n_mines(self):
        return (self >> 4)

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
        default=0)

    @GObject.Property(
        nick='Type Character',
        blurb='The character representing the cell type',
        type=str,
        flags=GObject.ParamFlags.READWRITE)
    def type_char(self):
        # if self.type & MineSweeperCellType.OPEN <= 1: # closed
        #     return ''

            # return self.type >> 4
        if self.is_closed():
            return ' '
        if self.is_mine():
            return '💣'
        if self.is_open():
            res = self.type >> 4
            return f'{res}' if res else '0'


        # elif self.type & MineSweeperCellType.CHECKED > 1: # checked
        #     return '⚑'

        raise TypeError(f'Cell has non-valid type! type={self.type:b}')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fill_mine(self) -> None:
        self.type |= MineSweeperCellType.MINE
        self.notify('type_char')

    def is_mine(self) -> bool:
        return bool(self.type & MineSweeperCellType.MINE)

    def fill_mines(self, n: int) -> None:
        # avoid the first 4 bits!
        self.type = self.type | (n << 4)
        self.notify('type_char')

    def open(self) -> None:
        self.type |= MineSweeperCellType.OPEN
        self.notify('type_char')

    def is_open(self) -> bool:
        return bool(self.type & MineSweeperCellType.OPEN)

    def is_empty(self) -> bool:
        return not self.is_mine()

    def is_closed(self) -> bool:
        return not self.is_open()
