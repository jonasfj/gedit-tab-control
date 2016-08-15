# TabControl, Gedit plugin to switch tabs with Ctrl (+ Shift) + Tab, and close with Ctrl + F4
# Copyright (C) 2012  Jonas Finnemann Jensen <jopsen@gmail.com>
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

from gi.repository import GObject, Gedit, Gdk

class TabControl(GObject.Object, Gedit.WindowActivatable):
	__gtype_name__ = 'TabControl'

	window = GObject.property(type=Gedit.Window)
	def __init__(self):
		GObject.Object.__init__(self)

	def do_activate(self):
		self.conn_id = self.window.connect("key-press-event", self.key_press)

	def do_deactivate(self):
		self.window.disconnect(self.conn_id)

	def do_update_state(self):
		pass

	def key_press(self, window, event):
		if event.state & Gdk.ModifierType.CONTROL_MASK == 0:
			return False
		shift = event.state & Gdk.ModifierType.SHIFT_MASK != 0
		# Close if Control + F4
		if not shift and Gdk.keyval_name(event.keyval) == 'F4':
			tab = window.get_active_tab()
			window.close_tab(tab)
			return True
		# Change tab with Control (Shift) Tab
		if Gdk.keyval_name(event.keyval) in ('ISO_Left_Tab', 'Tab'):
			tab = window.get_active_tab()
			tabs = tab.get_parent().get_children()

			if len(tabs) > 1 and tab in tabs:
				i = 1
				if shift:
					i = -1
				next = tabs[(tabs.index(tab) + i) % len(tabs)]
				window.set_active_tab(next)
			return True
		return False
