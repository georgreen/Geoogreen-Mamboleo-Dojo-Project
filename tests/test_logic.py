import os
import unittest

from core import logic
from models import model


class TestCreateRoom(unittest.TestCase):

    def setUp(self):
        self.dojo = model.Dojo("Andela-Kenya")
        self.white_char_in_name = logic.create_room('office', "name ",
                                                    self.dojo)
        self.white_char_in_typr = logic.create_room('livingspace ', "name",
                                                    self.dojo)

    def test_create_room_office(self):
        new_office = logic.create_room('office', 'orange',
                                       self.dojo)
        self.assertIsInstance(new_office, model.Office)

    def test_create_room_livingspace(self):
        new_livingspace = logic.create_room('livingspace', 'manjaro',
                                            self.dojo)
        self.assertIsInstance(new_livingspace, model.LivingSpace)

    def test_create_room_Wrongtype(self):
        with self.assertRaises(TypeError):
            logic.create_room('wrongname', 'gooodname', self.dojo)

    def test_create_room_Noname(self):
        self.assertEqual(logic.create_room('office', ' ',
                                           self.dojo),
                         'Invalid name')

    def test_white_char_in_name(self):
        self.assertEqual(self.white_char_in_name.name, "name")

    def test_white_char_in_type(self):
        self.assertIsInstance(self.white_char_in_typr, model.LivingSpace)


class TestAddPerson(unittest.TestCase):
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
        self.assertIsInstance(logic.add_person(("newstaff", "name2"), 'staff'),
                              model.Staff)
        self.assertIsInstance(logic.add_person(("newfellow", "name2"),
                                               'fellow'), model.Fellow)
        self.assertIsInstance(logic.add_person(("newfellow", "livingspace"),
                                               "fellow", "Y"), model.Fellow)

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            logic.add_person(("news", "taff"), [])
        with self.assertRaises(TypeError):
            logic.add_person(("new ", "fellow"), {})
        with self.assertRaises(TypeError):
            logic.add_person("newfellow", "fellow", 4)
        with self.assertRaises(TypeError):
            logic.add_person("newperson", "stafFell")

    def test_non_stanard_input(self):
        self.assertEqual(logic.add_person((" ", ""), "staff"), 'Invalid name')
        self.assertEqual(logic.add_person(("newname  ", "name2"),
                                          "fellow", "Y").name, "newname name2")
        self.assertEqual(logic.add_person((";;;;;;@@@", "]]]]]"), 'fellow'),
                         "Invalid name")


class TestListpplInroom(unittest.TestCase):
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

        # update rooms with staffself.dojo,
        self.room1.add_occupant(self.person1)
        self.room1.add_occupant(self.person2)

        self.person3 = model.Fellow("person3")
        self.person4 = model.Fellow("person4")

        # update room with fellows
        self.room1.add_occupant(self.person3)
        self.room2.add_occupant(self.person4)

        self.dojo = model.Dojo("Andela_kenya")
        self.dojo.add_staff(self.person1)
        self.dojo.add_staff(self.person2)
        self.dojo.add_fellow(self.person3)
        self.dojo.add_fellow(self.person4)

        self.dojo.add_office(self.room1)
        self.dojo.add_office(self.room5)
        self.dojo.add_livingspace(self.room2)

    def test_not_found(self):
        with self.assertRaises(logic.NotFoundException):
            logic.people_inroom(self.dojo, self.room4.name)
        with self.assertRaises(logic.NotFoundException):
            logic.people_inroom(self.dojo, self.room3.name)

    def test_room_found(self):
        self.assertEqual([self.person1, self.person2, self.person3],
                         logic.people_inroom(self.dojo, self.room1.name))
        self.assertEqual([self.person4],
                         logic.people_inroom(self.dojo, self.room2.name))

    def test_empty_rooom(self):
        self.assertEqual([], logic.people_inroom(self.dojo, self.room5.name))


class TestListUnallocated(unittest.TestCase):
    def setUp(self):
        self.dojo = model.Dojo("Andela_kenya")

        # unallocated staff
        self.staff1 = model.Staff("staff1")
        self.staff2 = model.Staff("staff2")

        # unallocated fellow
        self.fellow1 = model.Fellow("fellow1")
        self.fellow2 = model.Fellow("fellow2")

        self.office1 = model.Office("office1")
        self.livingspace1 = model.LivingSpace("livingspace1")

        # update dojo with infomation
        self.dojo.add_office(self.office1)
        self.dojo.add_livingspace(self.livingspace1)
        self.dojo.add_fellow(self.fellow1)
        self.dojo.add_fellow(self.fellow2)
        self.dojo.add_staff(self.staff1)
        self.dojo.add_staff(self.staff2)

    def test_unalloacted_staff(self):
        list_unallocated = logic.list_unallocated(self.dojo)
        self.assertTrue(self.staff1 in list_unallocated)
        self.assertTrue(self.staff2 in list_unallocated)

    def test_unallocated_fellow(self):
        list_unallocated = logic.list_unallocated(self.dojo)
        self.assertTrue(self.fellow1 in list_unallocated)
        self.assertTrue(self.fellow2 in list_unallocated)

    def test_not_unallocated_staff(self):
        self.staff1.office = True
        list_unallocated = logic.list_unallocated(self.dojo)
        self.assertTrue(self.staff1 not in list_unallocated)

    def test_not_unallocated_fellow(self):
        self.fellow1.office = True
        list_unallocated = logic.list_unallocated(self.dojo)
        self.assertTrue(self.fellow1 not in list_unallocated)

        self.fellow1.wants_living = True
        list_unallocated = logic.list_unallocated(self.dojo)
        self.assertTrue(self.fellow1 in list_unallocated)

        self.fellow1.livingspace = True
        list_unallocated = logic.list_unallocated(self.dojo)
        self.assertTrue(self.fellow1 not in list_unallocated)


class TestAllocations(unittest.TestCase):
    def setUp(self):
        self.dojo = model.Dojo("Andela-kenya")

        self.office = model.Office("Tsavo")
        self.livingspace = model.LivingSpace("hostel")

        self.staff1 = model.Staff("staff1")
        self.fellow1 = model.Fellow("fellow1")

        self.dojo.add_office(self.office)
        self.dojo.add_livingspace(self.livingspace)

    def test_office_allocation(self):
        dict_allocation = logic.dict_allocations(self.dojo)
        self.assertTrue(self.office.name in dict_allocation)
        self.assertTrue(len(dict_allocation[self.office.name]) == 0)

        self.office.add_occupant(self.fellow1)
        self.office.add_occupant(self.staff1)
        dict_allocation = logic.dict_allocations(self.dojo)
        self.assertTrue(self.fellow1 in dict_allocation[self.office.name])

    def test_livingspace_allocation(self):
        dict_allocation = logic.dict_allocations(self.dojo)
        self.assertTrue(self.livingspace.name in dict_allocation)
        self.assertTrue(len(dict_allocation[self.office.name]) == 0)

        self.livingspace.add_occupant(self.fellow1)
        dict_allocation = logic.dict_allocations(self.dojo)
        self.assertTrue(self.fellow1 in dict_allocation[self.livingspace.name])


class TestLoadPeople(unittest.TestCase):
    def setUp(self):
        self.dojo = model.Dojo("Andela_kenya")

    def test_load_people_file_not_found(self):
        msg = logic.load_data_txt("non_existent_file.txt", self.dojo)[0]
        self.assertTrue(msg['status'] == 'filenotfound')

    def test_load_people_file_exist(self):
        msg = logic.load_data_txt("file.txt", self.dojo)[0]
        self.assertTrue(msg['status'] == 'ok')


class TestSavePeople(unittest.TestCase):
    def setUp(self):
        self.staff1 = model.Staff("saveSTaff1")
        self.fellow1 = model.Fellow("saveFellow1")

    def test_save_txt(self):
        unallocated_list = [self.staff1, self.fellow1]
        logic.save_txt("filename.txt", unallocated_list)
        self.assertTrue(os.path.exists("filename.txt"))
