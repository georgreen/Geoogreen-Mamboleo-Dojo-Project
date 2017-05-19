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
    def setUp(self):
        self.dojo = model.Dojo("Andela-Kenya1")

    def test_throw_exception_non_string(self):
        with self.assertRaises(TypeError):
            self.dojo.load_state([])

        with self.assertRaises(TypeError):
            self.dojo.load_state(123456)

    def test_loads_given_previous_state(self):
        self.dojo.laod_state(previous_state=True)
        self.assertEquals(self.dojo.date, )

    def test_loads_give_path_existing(self):
        self.dojo.load_state("./db/sqlite.db")
        self.assertTrue(self.dojo.loaded)

    def test_throw_exception_nonexsting_path(self):
        with self.assertRaises(DBDoesNotExistException):
            self.dojo.load_state("./db/doesnotexist.db")

    def test_correct_content_type(self):
        pass

    def test_throw_exception_bad_content(self):
        pass

    def test_over_write_internal_state(self):
        pass

    def test_handles_large_file(self):
        pass

    def test_throw_exception_missing_fields(self):
        pass

    def test_throw_exception_on_already_loaded_db(self):
        pass
