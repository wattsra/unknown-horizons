# ###################################################
# Copyright (C) 2012 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

from tests.gui import gui_test


@gui_test(use_dev_map=True, timeout=120)
def test_ticket_1342(gui):
	"""
	Ship list widget (F3, formerly F4) crashes game on access.
	"""

	assert gui.find(name='ships_list') is None
	gui.press_key(gui.Key.F3)
	assert gui.find(name='ships_list')
	gui.press_key(gui.Key.F3)
	assert gui.find(name='ships_list') is None


@gui_test(use_dev_map=True, timeout=60)
def test_chat(gui):
	"""Opens chat dialog.

	NOTE: Doesn't test if anything was send, just checking that nothing
	crashes.
	"""

	assert not gui.find(name='chat_dialog_window')
	gui.press_key(gui.Key.C)
	assert gui.find(name='chat_dialog_window')
	gui.trigger('chat_dialog_window', 'cancelButton')
	assert not gui.find(name='chat_dialog_window')

	gui.press_key(gui.Key.C)
	assert gui.find(name='chat_dialog_window')
	gui.find('msg').write('Hello World')
	gui.trigger('chat_dialog_window', 'okButton')
	assert not gui.find(name='chat_dialog_window')
