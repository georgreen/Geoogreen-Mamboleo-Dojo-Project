import unittest

from core import logic
from models import model


class TestCreateAndAddroom(unittest.TestCase):
    def setUp(self):
        self.dojo = model.Dojo("Andela-kenya")

    def test_success_message(self):
        msg = logic.create_and_addroom(self.dojo, "office", "red")
        self.assertTrue(msg['status'] == "ok")

        msg = logic.create_and_addroom(self.dojo, "livingspace", "blue")
        self.assertTrue(msg['status'] == "ok")

    def test_error_message(self):
        msg = logic.create_and_addroom(self.dojo, "office", " ")
        self.assertTrue(msg['status'] == 'Invalid name')

        msg = logic.create_and_addroom(self.dojo, "", "new_room")
        self.assertTrue(msg['status'] == "failed")

        msg = logic.create_and_addroom(self.dojo, "office", "red")
        msg = logic.create_and_addroom(self.dojo, "office", "red")
        self.assertTrue(msg['status'] == "Duplicate name")


class TestAddspersonChooseroom(unittest.TestCase):
    def setUp(self):
        self.dojo = model.Dojo("Andela-kenya")

    def test_success_message(self):
        msg = logic.addsperson_chooseroom(self.dojo, "firstname",
                                          "secondname", "fellow",
                                          choice_live='N')

        self.assertTrue(msg['status'] == "ok")

        msg = logic.addsperson_chooseroom(self.dojo, "firstname",
                                          "secondname", "fellow",
                                          choice_live='Y')

        self.assertTrue(msg['status'] == "ok")

        msg = logic.addsperson_chooseroom(self.dojo, "firstname",
                                          "secondname", "staff",)

        self.assertTrue(msg['status'] == "ok")

    def test_error_mesage(self):
        msg = logic.addsperson_chooseroom(self.dojo, "first&*@",
                                          "###%", "fellow",
                                          choice_live='N')

        self.assertTrue(msg['status'] == "Invalid name")

        msg = logic.addsperson_chooseroom(self.dojo, "firstname",
                                          "secondname", "random_type",
                                          choice_live='N')

        self.assertTrue(msg['status'] == "Failed")

        msg = logic.addsperson_chooseroom(self.dojo, "firstname",
                                          "secondname", "fellow",
                                          choice_live='Random_choice')

        self.assertTrue(msg['status'] == "Invalid choice")


class TestReallocate(unittest.TestCase):
    def setUp(self):
        model.Person.number_of_person = 0
        self.dojo = model.Dojo("Andela_kenya")
        # allocated persons
        self.person1 = model.Staff("person1")
        self.person4 = model.Fellow("person4")
        # unallocated persons
        self.person2 = model.Staff("person2")
        self.person3 = model.Fellow("person3")

        self.room1 = model.Office("room1")
        self.room2 = model.LivingSpace("room2")

        self.room3 = model.Office("room3")
        self.room4 = model.LivingSpace("room4")

        # assing offices
        self.room1.add_occupant(self.person1)
        self.room1.add_occupant(self.person4)
        # assign livingspace
        self.room2.add_occupant(self.person4)

        self.person1.office = True
        self.person4.office = True
        self.person4.livingspace = True

        self.dojo.add_office(self.room1)
        self.dojo.add_livingspace(self.room2)
        self.dojo.add_office(self.room3)
        self.dojo.add_livingspace(self.room4)

        self.dojo.add_staff(self.person1)
        self.dojo.add_staff(self.person2)
        self.dojo.add_fellow(self.person3)
        self.dojo.add_fellow(self.person4)

    def test_reallocate_fellow_office(self):
        logic.reallocate_person(self.room3.name, self.person4.id, self.dojo)
        self.assertTrue(self.person4 in self.room3.occupants)

    def test_reallocate_fellow_livingspace(self):
        # import pdb; pdb.set_trace()
        logic.reallocate_person(self.room4.name, self.person4.id, self.dojo)
        self.assertTrue(self.person4 not in self.room4.occupants)

        self.person4.wants_living = True
        self.person4.livingspace = True
        logic.reallocate_person(self.room4.name, self.person4.id, self.dojo)
        self.assertTrue(self.person4 in self.room4.occupants)

    def test_reallocate_staff_office(self):
        logic.reallocate_person(self.room3.name, self.person1.id, self.dojo)
        self.assertTrue(self.person1 in self.room3.occupants)

    def test_reallocate_staff_livingspace(self):
        logic.reallocate_person(self.room4.name, self.person1.id, self.dojo)
        self.assertTrue(self.person1 not in self.room4.occupants)

    def test_reallocated_unallocated_person(self):
        logic.reallocate_person(self.room3.name, self.person2.id, self.dojo)
        self.assertTrue(self.person2 in self.room3.occupants)

        logic.reallocate_person(self.room3.name, self.person3.id, self.dojo)
        self.assertTrue(self.person3 in self.room3.occupants)

        logic.reallocate_person(self.room2.name, self.person3.id, self.dojo)
        self.assertTrue(self.person3 not in self.room2.occupants)

        self.person3.wants_living = True
        self.person3.livingspace = True
        logic.reallocate_person(self.room2.name, self.person3.id, self.dojo)
        self.assertTrue(self.person3 in self.room2.occupants)

    def test_reallocate_missing_room(self):
        msg = logic.reallocate_person("fake", self.person1.id, self.dojo)
        self.assertEquals(msg['message'], "Room not found")

    def test_reallocate_non_existing_person(self):
        msg = logic.reallocate_person(self.room4.name, "fake", self.dojo)
        self.assertEquals(msg['message'], "Invalid  User Id")

        msg = logic.reallocate_person(self.room4.name, 100, self.dojo)
        self.assertEquals(msg['message'], "Person not found")
