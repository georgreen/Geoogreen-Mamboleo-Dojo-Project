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

    class test_list_ppl_inroom(unittest.TestCase):
        """
        Testing strategy
        partitioons:
            @input
            room_name
                 -> len(input) -> 0 , postive,
                 -> name : whitespace, str(number), asscii charcters
                 --> bad types
            list_rooms
                  len(list_rooms) 0, positive, odd , even
                  contains[query] : ~contains[query]
            @output
            Each test should be covered atleast once
        """
        def setUp(self):
            self.room1 = model.Office("room1")
            self.room2 = model.LivingSpace("room2")
            self.room3 = model.Office("notindojo")
            self.room4 = model.LivingSpace("notindojo")
            self.room5 = model.Office("emptyroom")

            self.person1 = model.Staff("person1")
            self.person2 = model.Staff("person2")

             #update rooms with info
            self.room1.add_occupant(self.person1)
            self.room1.add_occupant(self.person2)


            self.person3 = model.Fellow("person3")
            self.person4 = model.Fellow("person4")

            #update room with fellows
            self.room1.add_occupant(self.person3)
            self.room2.add_occupant(self.person4)

            self.dojo = model.Dojo("Andela_kenya")
            self.dojo.add_staff(person1)
            self.dojo.add_staff(person2)
            self.dojo.add_fellow(person3)
            self.dojo.add_fellow(person4)

            self.dojo.add_office(self.room1)
            self.dojo.add_office(self.room5)
            self.add_livingspace(self.room2)

        def test_not_found(self):
            with self.assertRaises(NotFoundException):
                logic.people_inroom(self.room4.name)
            with self.assertRaises(NotFoundException):
                logic.people_inroom(self.room3.name)

        def test_room_found(self):
            self.assertEqual([self.person1, self.person2, self.person3], logic.people_inroom(self.room1.name))
            self.assertEqual([self.person4], logic.people_inroom(self.room2.name))

        def test_empty_rooom(self):
            self.assertEqual([], logic.people_inroom(self.room5.name))


class test_list_unallocated(unittest.TestCase):
    def setUp(self):
        self.dojo = model.Dojo("Andela_kenya-zero")
        self.person1 = model.Staff("person1")
        self.person2 = model.Staff("person2")
        self.person3 = model.Staff("person3")

        self.dojo.add_staff(self.person1)
        self.dojo.add_staff(self.person2)
        self.dojo.add_staff(self.person3)

        self.dojo1 = model.Dojo("Andela")
        self.person4 = model.Fellow("person4")
        self.person4.office = True
        self.person4.livingspace = True
        self.person5 = model.Fellow("person5")
        self.person5.office = False
        self.person5.livingspace = True
        self.person6 = model.Fellow("person6")
        self.person6.livingspace = False
        self.person6.office = True

        self.dojo1.add_fellow(self.person4)
        self.dojo1.add_fellow(self.person5)
        self.dojo1.add_fellow(self.person6)

        self.dojo2 = model.Dojo("Andela-Kenya-two")
        self.dojo2.add_fellow(self.person6)
        self.dojo2.add_staff(self.person1)

    def  test_feat_list_unallocated(self):
        #test fellow and staff mixed states
        self.assertEqual([self.person5,self.person6 ], logic.list_unallocated(self.dojo1))
        #test all not allocated staff
        self.assertEqual([self.person1, self.person2,self.person3], logic.list_unallocated(self.dojo))
        #test fellow
        self.assertEqual([self.person6,self.person1], logic.list_unallocated(self.dojo2))
