from context import core
from context import models

from models import model
from core import logic

import unittest

class test_logic(unittest.TestCase):
	def test_create_room_office(self):
		new_office = logic.create_room('office', 'orange')
		self.assertIsInstance(new_office, model.Office)

	def test_create_room_livingspace(self):
		new_livingspace = logic.create_room('livingspace', 'manjaro')
		self.assertIsInstance(new_livingspace, model.LivingSpace)

	def test_create_room_Wrongtype(self):
		self.assertRaises(TypeError, logic.create_room('wrongname', 'orange'))

	def test_create_room_Noname(self):
		self.assertEqual(logic.create_room('office', ' '), 'Invalid name')
