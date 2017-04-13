from context import models

from models import model


import unittest

class test_Rooms(unittest.TestCase):
    """
    Testing strategy
    partitioons:
        name -> len(name) -> 0 , postive,
             -> name : whitespace, str(number), asscii charcters
             -> name : duplicates
             -->  bad types
        max_population -> 0, postive, negative
                        -> bad type str, dict
        Each should be covered atleast once
    """
    def setUp(self):
        self.room = model.Room(20, 'new_room')
        self.room1 = model.Room(6, 'new_room1')
        self.livingspace = model.LivingSpace('orange')
        self.office = model.Office('manjaro')

    def test_Room_instance(self):
        self.assertIsInstance(self.room, model.Room)
        self.assertIsInstance(self.room1, model.Room)

    #covers max_population > 0
    def test_Room_max_occupation(self):
        self.assertEqual(20, self.room.max_occupants)

    def test_Room_name(self):
        self.assertEqual('new_room1', self.room1.name)
        self.room1.name = "changedname"
        self.assertEqual('changedname', self.room1.name)

    def test_office_ocupants(self):
        self.assertEqual(6, self.office.max_occupants)

    def test_livingspace_ocupants(self):
        self.assertEqual(4, self.livingspace.max_occupants)

    def test_sublclass_Room(self):
        self.assertTrue(issubclass(model.Office, model.Room))
        self.assertTrue(issubclass(model.LivingSpace, model.Room))

    def test_room_current_population(self):
        self.assertEqual(self.room.current_population, 0)


class test_person(unittest.TestCase):
    """
    Testing strategy
    partitioons:
        @properties
        name , office

             -> len(name) -> 0 , postive,
             -> name : whitespace, str(number), asscii charcters
             -> name : duplicates
             -->  bad types
        @methods

        Each test should be covered atleast once
    """
    def setUp(self):
        model.Person.number_of_person = 0
        model.Staff.number_of_staff = 0
        model.Fellow.number_of_fellows = 0

        self.person1 = model.Person("person1")
        self.person2 = model.Person("person2")

        self.fellow1 = model.Fellow("fellow1")
        self.fellow2 = model.Fellow("fellow2", True)


        self.staff1 = model.Staff("staff1")
        self.staff2 = model.Staff("staff2")

        self.office = model.Office("testme")
        self.office1 = model.Office("HR")

        self.livingspace = model.Office('Orange')
        self.livingspace1 = model.Office('manjaro')

        self.fellow2.office = self.office1
        self.fellow2.livingspace = True


    def test_person_instance(self):
        new_person = model.Person("new_person")
        self.assertIsInstance(new_person, model.Person)

    def test_add_office(self):
        self.person1.office = self.office
        self.staff2.office = self.office1
        self.fellow1.office = self.office

        self.assertEqual([self.person1.office, self.fellow1.office], [self.office, self.office])
        self.assertEqual(self.staff2.office, self.office1)

    def test_remove_office(self):
        self.person1.remove_office()
        self.assertEqual(self.person1.office, None)

    def test_is_allocated_office(self):
        self.assertEqual(self.person1.is_allocated_office(), False)

    def test_number_of_person(self):
        self.assertEqual(model.Person.number_of_person, 6)

    def test_number_of_staff(self):
        self.assertEqual(model.Staff.number_of_staff, 2)

    def test_fellow_add_living(self):
        self.assertEqual(self.fellow2.livingspace, True)

    def test_fellow_is_allocated_living(self):
        self.assertEqual(self.fellow2.is_allocated_living(), True)
        self.assertNotEqual(self.fellow1.is_allocated_living(), True)

    def test_number_of_fellow(self):
        self.assertEqual(model.Fellow.number_of_fellows, 2)

    def test_fellow_wants_living(self):
        self.assertEqual(self.fellow2.wants_living, True)


class test_dojo(unittest.TestCase):
    """
    Testing strategy
    partitioons:
        @properties
        name , office, livingspace, fellow, staff

             -> len(name) -> 0 , postive,
             -> name : whitespace, str(number), asscii charcters
             -> name : duplicates
             -->  bad types
        @methods
        is_staff, remove_office, remove_livingspace, remove_fellow, remove_staff
        input : -> data bot in dojo, data in dojo,
               ->   bad types, double

        Each test should be covered atleast once
    """
    def setUp(self):
        model.Dojo.facillity_names.clear()
        self.dojo1 = model.Dojo("Andela_kenya")

        self.room = model.Office("HR")
        self.room2 = model.Office("IT")

        self.room3 = model.LivingSpace("Complex_A")
        self.room4 = model.LivingSpace("Complex_B")

        self.person1 = model.Fellow("Morris")
        self.person2 = model.Fellow("new_Fellow", True)

        self.person3 = model.Staff("Ndiga")
        self.person4 = model.Staff("Someone")

        #############update dojo with info###########
        self.dojo1.add_office(self.room)
        self.dojo1.add_office(self.room2)
        self.dojo1.add_livingspace(self.room3)
        self.dojo1.add_livingspace(self.room4)
        self.dojo1.add_staff(self.person3)
        self.dojo1.add_staff(self.person4)


    #test badtype as name input
    def test_badtypes_name(self):
        with self.assertRaises(TypeError):
            model.Dojo([])
        with self.assertRaises(TypeError):
            model.Dojo(1)

    #test non-stanard input on iput -> name
    def test_whitespace_ascii_name(self):
        with self.assertRaises(TypeError):
             model.Dojo("  ")
        with self.assertRaises(TypeError):
             model.Dojo('@#####')


        self.assertEqual('@#####F', model.Dojo('@#####F').name)
        self.assertEqual("Hello", model.Dojo("Hello      ").name)

    #test making duplicate dojo
    def test_duplicate_name(self):
        with self.assertRaises(model.DuplicateError):
            model.Dojo("Andela_kenya")

    #covers len(name) > 0
    def test_name_len_positive(self):
        self.assertIsInstance( model.Dojo("my_cool_name"), model.Dojo)
    #cover len(name) == 0, name = ''
    def test_name_len_zero(self):
        with self.assertRaises(TypeError):
            model.Dojo('')


    #cover is_staff
    def test_is_staff(self):
        self.assertTrue(self.dojo1.is_staff(self.person3))
        self.assertFalse(self.dojo1.is_staff(model.Staff("stranger")))
    #cover_remove_office
    def test_remove_office(self):
        self.dojo1.remove_office(self.room)
        self.assertFalse(self.room in self.dojo1.office)

    #covers remove_livingspace
    def test_remove_livingspace(self):
        self.dojo1.remove_livingspace(self.room3)
        self.assertFalse(self.room3 in self.dojo1.livingspace)
    #covers remove_staff
    def test_remove_staff(self):
        self.dojo1.remove_staff(self.person4)
        self.assertFalse(self.person4 in self.dojo1.staff)
    #covers remove_fellow
    def test_remove_fellow(self):
        self.dojo1.remove_fellow(self.person2)
        self.assertFalse(self.person2 in self.dojo1.fellow)
