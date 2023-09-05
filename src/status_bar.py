# status_bar.py

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


from typing import cast
from gi.repository import GLib, GObject, Gtk

import time


@Gtk.Template(resource_path='/com/github/adr/MineSweeper/status-bar.ui')
class MineSweeperStatusBar(Gtk.Widget):
    """
    The status bar of the game.

    This is the top bar of the main content, it displays
    a simley face and a timer.
    """

    __gtype_name__ = 'MineSweeperStatusBar'

    timer = GObject.Property(
        nick='Timer',
        blurb='Seconds timer',
        flags=GObject.ParamFlags.READWRITE,
        type=str,
    )

    box = cast(Gtk.Box, Gtk.Template.Child())

    SEC = 1
    restart_button_added = False
    timeout_id = 0
    face = GObject.Property(nick="Face",
                            blurb="The face showen in the top status bar.",
                            flags=GObject.ParamFlags.READWRITE,
                            type=str,
                            default='😼')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_timer()

        self.restart_button = Gtk.Button(label='RESTART', action_name='app.reload')

    def update_content(self):
        self._init_timer()
        self.face = '😼'
        if self.restart_button_added:
            self.box.remove(self.restart_button)

    def update_timer(self):
        self.elapsed_time += self.SEC
        self.timer = time.strftime('%M:%S', time.localtime(self.elapsed_time))

        return True             # keep rolling

    def _init_timer(self):
        self.start_time = time.localtime()
        self.elapsed_time = 0
        self.timer = time.strftime('%M:%S', time.localtime(self.elapsed_time))

        if self.timeout_id:
            GLib.source_remove(self.timeout_id)
        self.timeout_id = GLib.timeout_add_seconds(self.SEC, self.update_timer)

    def add_restart_button(self, _widget):
        self.restart_button_added = True
        self.face = '😿'
        self.box.append(self.restart_button)
