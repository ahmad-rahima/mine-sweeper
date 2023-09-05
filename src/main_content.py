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

    gesture = Gtk.GestureLongPress(delay_factor=1)
    settings = Gio.Settings(schema_id="com.github.adr.MineSweeper")

    cells_column = GObject.Property(
        nick='Cells Column',
        blurb='The number of cells per column',
        type=int,
        flags=GObject.ParamFlags.READWRITE,
        default=4
    )

    cells_row = GObject.Property(
        nick='Cells Row',
        blurb='The number of cells per row',
        type=int,
        flags=GObject.ParamFlags.READWRITE,
        default=4
    )

    mines_no = GObject.Property(
        nick='Mines NO',
        blurb='The number of mines in the grid.',
        type=int,
        flags=GObject.ParamFlags.READWRITE,
        default=3
    )

    grid_view = cast(Gtk.GridView, Gtk.Template.Child())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = Gtk.Application.get_default()
        app.create_action('reload', self.update_content)
        app.set_accels_for_action("app.reload", ['<Control>r'])

        self.add_controller(self.gesture)
        self.gesture.connect('pressed', lambda *_: print('Pressed!'))

    def update_content(self, _, __):
        self.cells_column = self.settings.get_int('cells-column')
        self.cells_row = self.settings.get_int('cells-row')
        self.mines_no = self.settings.get_int('mines-no')

        self._init_grid()
        self._init_cell_mines()
        self._init_cell_neighbours()

    def _init_grid(self):
        self.cells = Gio.ListStore(item_type=MineSweeperCell)
        for _ in range(self.cells_column * self.cells_row):
            cell = MineSweeperCell()
            cell.type = 0
            self.cells.append(cell)

    def _init_cell_mines(self):
        for cell in sample(list(self.cells), k=self.props.mines_no):
            cell.fill_mine()

    def _init_cell_neighbours(self):
        for i in range(self.cells_column):
            for j in range(self.cells_row):
                cell = cast(MineSweeperCell, self.cells.get_item(j * self.cells_column + i))
                assert cell, "None is not valid for Cell."

                mines = [self.cells.get_item(j * self.cells_column + i)
                         for _i in range(max(i-1, 0), min(i+2, self.cells_column))
                         for _j in range(max(j-1, 0), min(j+2, self.cells_row))
                         if self.cells.get_item(_j * self.cells_column + _i).is_mine()]
                mines_no = len(mines)
                assert mines_no >= 0, 'Mines number at least is 0.'

                cell.fill_mines(mines_no)

    @Gtk.Template.Callback()
    def on_grid_activate(self, gridview: Gtk.GridView, pos: int):
        cell = cast(MineSweeperCell, self.cells.get_item(pos))
        cell.open()

        # if cell.is_mine():
        #     self.emit('mine')

        # print('Activating..', pos, '. cell: ', cell)

    @Gtk.Template.Callback()
    def on_grid_selection(
            self,
            selection_model: Gtk.SelectionModel,
            pos: int,
            n_items: int
    ):
        print('Selecting..')
