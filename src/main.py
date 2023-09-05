# main.py
#
# Copyright 2023 Ahmad Rahima
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
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib, GObject, Gdk, Gtk, Gio, Adw
from .window import MineSweeperWindow


class MineSweeperApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.github.adr.MineSweeper',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('configuration_4x4x3', self.on_configuration_4x4x3_action)
        self.create_action('configuration_8x8x10', self.on_configuration_8x8x10_action)
        self.create_action('configuration_16x16x40', self.on_configuration_16x16x40_action)

        self.settings = Gtk.Settings.get_default()
        assert self.settings, "Default settings can not be None."

        self._load_style_sheet()

    def _load_style_sheet(self):
        self.display = Gdk.Display.get_default()
        assert(self.display)

        style_provider = Gtk.CssProvider()
        style_provider.load_from_resource(resource_path='/com/github/adr/MineSweeper/style.css')

        Gtk.StyleContext.add_provider_for_display(
            self.display,
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.style_provider = Gtk.CssProvider()
        self.settings.connect('notify::gtk-application-prefer-dark-theme', self.set_style_mode)

    def on_configuration_4x4x3_action(self, widget, _):
        settings = Gio.Settings(schema_id="com.github.adr.MineSweeper")
        settings.set_int('cells-column', 4)
        settings.set_int('cells-row', 4)
        settings.set_int('mines-no', 3)

        self.get_active_window().activate_action('app.reload')

    def on_configuration_8x8x10_action(self, widget, _):
        settings = Gio.Settings(schema_id="com.github.adr.MineSweeper")
        settings.set_int('cells-column', 8)
        settings.set_int('cells-row', 8)
        settings.set_int('mines-no', 10)

        self.get_active_window().activate_action('app.reload')

    def on_configuration_16x16x40_action(self, widget, _):
        settings = Gio.Settings(schema_id="com.github.adr.MineSweeper")
        settings.set_int('cells-column', 16)
        settings.set_int('cells-row', 16)
        settings.set_int('mines-no', 40)

        self.get_active_window().activate_action('app.reload')

    def set_style_mode(self, settings, e):
        dark_style = settings.get_property('gtk-application-prefer-dark-theme')
        style_mode = 'dark' if dark_style else 'light'

        self.style_provider.load_from_resource(
            resource_path=f'/com/github/adr/MineSweeper/{style_mode}_style.css'
        )
        Gtk.StyleContext.add_provider_for_display(
            self.display,
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = MineSweeperWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='mine-sweeper',
                                application_icon='com.github.adr.MineSweeper',
                                developer_name='Ahmad Rahima',
                                version='0.1.0',
                                developers=['Ahmad Rahima'],
                                copyright='© 2023 Ahmad Rahima')
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = MineSweeperApplication()
    return app.run(sys.argv)
