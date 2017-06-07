import os
import unittest

from models import model


class BaseTest(unittest.TestCase):
    def tearDown(self):
        self.database_dir = os.path.abspath("./models/database/")
        if os.path.exists(self.database_dir):
            for test_file in os.listdir(self.database_dir):
                path = self.database_dir + "/" + test_file
                os.remove(path)
            os.rmdir(self.database_dir)


class LoadStateTestCase(BaseTest):
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

    def setUp(self):
        self.dojo = model.Dojo("Andela-Kenya1")
        new_fellow = model.Fellow("new_fellow")
        new_staff = model.Staff("new_staff")

        new_office = model.Office("new_office")
        new_livingspace = model.LivingSpace("new_livingspace")
        self.dojo.save_state("sqlite.db")

        self.dojo1 = model.Dojo("Andela-Kenya2")
        self.dojo1.add_staff(new_staff)
        self.dojo1.add_fellow(new_fellow)
        self.dojo1.add_livingspace(new_livingspace)
        self.dojo1.add_office(new_office)

        self.dojo1.save_state("overideinternalstate.db")
        self.dojo1.save_state("alreadyloaded.db")

    def test_throw_exception_non_string(self):
        with self.assertRaises(TypeError):
            self.dojo.load_state([])

        with self.assertRaises(TypeError):
            self.dojo.load_state(123456)

    def test_loads_previous_state(self):
        self.dojo1.save_state("default.db")
        self.dojo.load_state(previous_state=True)
        self.assertTrue(self.dojo.loaded)

    def test_loads_give_path_existing(self):
        self.dojo.load_state("sqlite.db")
        self.assertTrue(self.dojo.loaded)

    def test_throw_exception_nonexsting_path(self):
        with self.assertRaises(model.DBDoesNotExistException):
            self.dojo.load_state("doesnotexist.db")

    def test_throw_exception_bad_content(self):
        pass


class SaveStateTestCase(BaseTest):
    """
    Testing strategy
    partitions:
        input: default, abitray string, non-string
        special case: DB already exists, over write existing db

        This should cover the full catersian
    """

    def setUp(self):
        self.dojo = model.Dojo("AndelaKenya_test")
        self.office = model.Office('new_office')
        self.livingspace = model.LivingSpace('new_livingspace')
        self.dojo.add_office(self.office)
        self.dojo.add_livingspace(self.livingspace)

        self.fellow = model.Fellow("new_fellow")
        self.staff = model.Staff("new_staff")
        self.dojo.add_fellow(self.fellow)
        self.dojo.add_staff(self.staff)
        self.database_dir = os.path.abspath("./models/database/")

    def test_creates_databse_with_abitaryname(self):
        self.dojo.save_state("sqlite.db")
        path = self.database_dir + "/sqlite.db"
        self.assertTrue(os.path.exists(path))

    def test_create_db_without_args(self):
        self.dojo.save_state()
        path = self.database_dir + "/default.db"
        self.assertTrue(os.path.exists(path))

    def test_throw_update_error_if_exists(self):
        # import pdb; pdb.set_trace()
        self.dojo.save_state("alreadyexist.db")
        with self.assertRaises(model.UpdateException):
            self.dojo.save_state("alreadyexist.db")

    def test_reject_non_string_input(self):
        with self.assertRaises(TypeError):
            self.dojo.save_state([])

        with self.assertRaises(TypeError):
            self.dojo.save_state(1234567)

    def test_overwrite_existing_db(self):
        self.dojo.save_state("existing.db")
        with self.assertRaises(model.OverWriteException):
            self.dojo.save_state("existing.db", over_write=True)
