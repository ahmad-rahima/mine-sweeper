# main_content.py

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


from functools import reduce
from typing import Iterable, cast
from gi.repository import GObject, Gtk, Gio
from random import sample

from .cell import MineSweeperCell, MineSweeperCellType

from . import status_bar


@Gtk.Template(resource_path='/com/github/adr/MineSweeper/main-content.ui')
class MineSweeperMainContent(Gtk.Widget):
    """
    MineSweeper Main content widget.

    This widget contains the real stuff.
    It contains:
    1. The Status bar of the game.
    2. And the grid of cells (which represent the game).
    """

    __gtype_name__ = 'MineSweeperMainContent'

    cells = GObject.Property(nick='Cells',
                             blurb='The contained cells of the grid.',
                             type=Gio.ListStore,
                             flags=GObject.ParamFlags.READWRITE)

    # TODO: change this later to settings
    WIDTH = 4
    HEIGHT = 4
    MINES_NO = 3
    gesture = Gtk.GestureLongPress(delay_factor=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._init_grid()
        self._init_cell_mines()
        self._init_cell_neighbours()
        self.add_controller(self.gesture)
        self.gesture.connect('pressed', lambda *_: print('Pressed!'))


    def _init_grid(self):
        self.cells = Gio.ListStore(item_type=MineSweeperCell)
        for _ in range(self.WIDTH * self.HEIGHT):
            cell = MineSweeperCell()
            cell.type = (MineSweeperCellType.EMPTY.value |
                         MineSweeperCellType.CLOSED.value)
            self.cells.append(cell)

    def _init_cell_mines(self):
        for cell in sample(list(self.cells), k=self.MINES_NO):
            cell.fill_mine()

    def _init_cell_neighbours(self):
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                cell = cast(MineSweeperCell, self.cells.get_item(j * self.WIDTH + i))
                assert cell, "None is not valid for Cell."

                mines = [self.cells.get_item(j * self.WIDTH + i)
                         for _i in range(max(i-1, 0), min(i+2, self.WIDTH))
                         for _j in range(max(j-1, 0), min(j+2, self.HEIGHT))
                         if self.cells.get_item(_j * self.WIDTH + _i).is_mine()]
                mines_no = len(mines)
                assert mines_no >= 0, 'Mines number at least is 0.'

                cell.fill_mines(mines_no)

    @Gtk.Template.Callback()
    def on_grid_activate(self, gridview: Gtk.GridView, pos: int):
        cell = cast(MineSweeperCell, self.cells.get_item(pos))
        cell.open()

        # if (cell.type >> 4) == MineSweeperCellType.MINE:
        #     print('You Lose!')

        print('Activating..', pos, '. cell: ', cell)

    @Gtk.Template.Callback()
    def on_grid_selection(
            self,
            selection_model: Gtk.SelectionModel,
            pos: int,
            n_items: int
    ):
            print('Selecting..')
