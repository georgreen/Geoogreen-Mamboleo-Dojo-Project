import os
import unittest

from models import model


class LoadStateTestCase(unittest.TestCase):
    """
    Testing strategy
    partitions:
        input:Previous state DB, path to DB, Correct content type, bad content,
               non-existant DB, bad input type(non-string)
        special case: Over write existing Internal state, Handle Large file,
                      Missing Fields in DB, Already Loaded Data,
                      Append DB state to internal state

        This should cover the full catersian plane
    """
    dojo = model.Dojo("Andela-Kenya1")
    dojo1 = model.Dojo("Andela-Kenya2")
    def setUp(self):
        self.dojo = LoadStateTestCase.dojo
        new_fellow = model.Fellow("new_fellow")
        new_staff = model.Staff("new_staff")

        new_office = model.Office("new_office")
        new_livingspace = model.LivingSpace("new_livingspace")

        self.dojo1 = LoadStateTestCase.dojo1
        self.dojo1.add_staff(new_staff)
        self.dojo1.add_fellow(new_fellow)
        self.dojo1.add_livingspace(new_livingspace)
        self.dojo1.add_office(new_office)


    def test_throw_exception_non_string(self):
        with self.assertRaises(TypeError):
            self.dojo.load_state([])

        with self.assertRaises(TypeError):
            self.dojo.load_state(123456)

    def test_loads_previous_state(self):
        self.dojo.laod_state(previous_state=True)
        self.assertTrue(self.dojo.loaded)

    def test_loads_give_path_existing(self):
        self.dojo.load_state("./db/sqlite.db")
        self.assertTrue(self.dojo.loaded)

    def test_throw_exception_nonexsting_path(self):
        with self.assertRaises(DBDoesNotExistException):
            self.dojo.load_state("./db/doesnotexist.db")

    def test_over_write_internal_state(self):
        with self.assertRaises(DBOverwriteExecption):
            self.dojo1("./db/overideinternalstate.db", overwrite=True)

    def test_throw_exception_on_already_loaded_db(self):
        with self.assertRaises(DBAlreadyLoadedException):
            self.dojo.load_state("./db/already_loaded.db")

    def test_handles_large_file(self):
        pass

    def test_throw_exception_bad_content(self):
        pass
