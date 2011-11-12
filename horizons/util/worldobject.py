# ###################################################
# Copyright (C) 2011 The Unknown Horizons Team
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

import weakref
import logging

from changelistener import ChangeListener

class WorldObjectNotFound(KeyError):
	pass

class WorldObject(ChangeListener):
	"""Gives every instance a unique id.
	"""
	__next_id = 1
	__objects = weakref.WeakValueDictionary()
	log = logging.getLogger("util.worldobject")
	def __init__(self, worldid=None, **kwargs):
		"""
		@param worldid: worldid to assign. Use None to get an autogenerated one.
		"""
		super(WorldObject, self).__init__(**kwargs)
		self.__init(worldid)

	def __init(self, worldid=None):
		self.worldid = worldid if worldid is not None else WorldObject.__next_id
		assert self.worldid not in WorldObject.__objects
		WorldObject.__objects[self.worldid] = self
		# Make sure that new WorldIDs are always higher than every other WorldObject
		WorldObject.__next_id = max(WorldObject.__next_id, self.worldid+1)

	@classmethod
	def get_object_by_id(cls, id):
		"""Returns the worldobject with id id
		Throws WorldObjectNotFound with the worldid as arg.
		"""
		try:
			return cls.__objects[id]
		except KeyError as e:
			raise WorldObjectNotFound(e.args[0])

	@classmethod
	def reset(cls):
		cls.__next_id = 1
		cls.__objects.clear()

	def save(self, db):
		pass

	def load(self, db, worldid):
		super(WorldObject, self).load(db, worldid)
		self.__init(worldid)
		self.log.debug('loading worldobject %s %s', worldid, self)

	def remove(self):
		super(WorldObject, self).remove()
		self.log.debug("Removing WorldObject %s %s", self.worldid, self)
		pass # removing is done implicitly by WeakValueDict

	def __lt__(self, other):
		return self.worldid < other.worldid

	# for testing:
	@classmethod
	def get_objs(self): return self.__objects
