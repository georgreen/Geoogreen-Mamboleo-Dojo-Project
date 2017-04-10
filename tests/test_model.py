from context import models

from models import model


import unittest

class test_logic_core(unittest.TestCase):
    def setUp(self):
        self.room = model.Room(20, 'new_room')
        self.room1 = model.Room(6, 'new_room1')
        self.livingspace = model.LivingSpace('orange')
        self.office = model.Office('manjaro')

    def test_Room_instance(self):
        self.assertIsInstance(self.room, model.Room)
        self.assertIsInstance(self.room1, model.Room)

    def test_Room_max_occupation(self):
        self.assertEqual(20, self.room.max_occupants)

    def test_Room_name(self):
        self.assertEqual('new_room1', self.room1.name)

    def test_office_ocupants(self):
        self.assertEqual(6, self.office.max_occupants)

    def test_livingspace_ocupants(self):
        self.assertEqual(4, self.livingspace.max_occupants)

    def test_sublclass_Room(self):
        self.assertTrue(issubclass(model.Office, model.Room))
        self.assertTrue(issubclass(model.LivingSpace, model.Room))
