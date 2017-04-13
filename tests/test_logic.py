from context import core
from context import models

from models import model

from core import logic

import unittest

class test_create_room(unittest.TestCase):
    def setUp(self):
        self.white_char_in_name = logic.create_room('office', "name        ")
        self.white_char_in_typr = logic.create_room('livingspace        ', "name")


    def test_create_room_office(self):
        new_office = logic.create_room('office', 'orange')
        self.assertIsInstance(new_office, model.Office)

    def test_create_room_livingspace(self):
        new_livingspace = logic.create_room('livingspace', 'manjaro')
        self.assertIsInstance(new_livingspace, model.LivingSpace)

    def test_create_room_Wrongtype(self):
        with self.assertRaises(TypeError):
            logic.create_room('wrongname', 'gooodname')

    def test_create_room_Noname(self):
        self.assertEqual(logic.create_room('office', ' '), 'Invalid name')

    def test_white_char_in_name(self):
        self.assertEqual(self.white_char_in_name.name, "name")

    def test_white_char_in_type(self):
        self.assertIsInstance(self.white_char_in_typr, model.LivingSpace)



class test_add_person(unittest.TestCase):
    """
    Testing strategy
    partitioons:
        @input
        name,person_type,
             -> len(input) -> 0 , postive,
             -> name : whitespace, str(number), asscii charcters
             --> bad types
               -> bad types, double
        livingspace
                -> True
                -> False
                -> bad type
        Each test should be covered atleast once
    """
    def test_create_person(self):
        self.assertIsInstance(logic.add_person(("newstaff","name2"), 'staff'), model.Staff)
        self.assertIsInstance(logic.add_person(("newfellow", "name2"), 'fellow'), model.Fellow)
        self.assertIsInstance(logic.add_person(("newfellow","livingspace"), "fellow", "Y"), model.Fellow)

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            logic.add_person(("news","taff"), [] )
        with self.assertRaises(TypeError):
            logic.add_person(("new ","fellow"), {})
        with self.assertRaises(TypeError):
            logic.add_person("newfellow", "fellow", 4)
        with self.assertRaises(TypeError):
            logic.add_person("newperson", "stafFell")

    def test_non_stanard_input(self):
        self.assertEqual(logic.add_person((" ", ""), "staff"), 'Invalid name')
        self.assertEqual(logic.add_person(("newname  ", "name2"), "fellow", "Y").name, "newname name2")
        self.assertEqual(logic.add_person((";;;;;;@@@", "]]]]]"), 'fellow'), "Invalid name")
