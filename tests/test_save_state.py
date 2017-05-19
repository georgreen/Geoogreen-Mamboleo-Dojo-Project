
import os
import unittest

from models import model


class SaveStateTestCase(unittest.TestCase):
    """
    Testing strategy
    partitions:
        input: default, abitray string, non-string
        special case: DB already exists, over write existing db

        This should cover the full catersian
    """
    dojo = model.Dojo("AndelaKenya_test")
    def setUp(self):
        self.dojo = SaveStateTestCase.dojo
        self.office = model.Office('new_office')
        self.livingspace = model.LivingSpace('new_livingspace')
        self.dojo.add_office(self.office)
        self.dojo.add_livingspace(self.livingspace)

        self.fellow = model.Fellow("new_fellow")
        self.staff = model.Staff("new_staff")
        self.dojo.add_fellow(self.fellow)
        self.dojo.add_staff(self.staff)

    def test_creates_databse_with_abitaryname(self):
        self.dojo.save_state("sqlite.db")
        self.assertTrue(os.path.exists("./db/sqlite.db"))

    def test_create_db_without_args(self):
        self.dojo.save_state()
        self.assertTrue(os.path.exists("./db/default.db"))

    def test_throw_update_error_if_exists(self):
        with self.assertRaises(UpdateException):
            self.dojo.save_state()

    def test_reject_non_string_input(self):
        with self.assertRaises(TypeError):
            self.dojo.save([])

        with self.assertRaises(TypeError):
            self.dojo.save(1234567)

    def test_overwrite_existing_db(self):
        with self.assertRaises(OverWriteException):
            self.save_state("existing.db", over_write=True)
