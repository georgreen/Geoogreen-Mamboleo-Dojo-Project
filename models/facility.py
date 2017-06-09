import os

from models.person import Person
from models.room import LivingSpace, Office, Room

from .base_db import (DBDoesNotExistException, OverWriteException,
                      UpdateException, create_session, create_tables,
                      load_engine)


class Dojo():
    """
    models Dojo facillity
    """

    def __init__(self, name):
        self.rooms = {'offices': {}, 'livingspace': {}}
        self.person = {'fellow': {}, 'staff': {}}
        self.name = name

        self.database_session = None
        self.database_engine = None
        self.db_migrations = True

        self.loaded = None
        self.database_name = None

    @property
    def livingspace(self):
        return self.rooms['livingspace'].values()

    @property
    def fellow(self):
        return self.person['fellow'].values()

    @property
    def staff(self):
        return self.person['staff'].values()

    @property
    def office(self):
        return self.rooms['offices'].values()

    @property
    def takken_names(self):
        return (list(self.rooms['offices'].keys()) +
                list(self.rooms['livingspace'].keys()))

    def add_person_office(self, name, staff):
        self.rooms['offices'][name].add_occupant(staff)

    def add_fellow_living(self, name, fellow):
        self.rooms['livingspace'][name].add_occupant(fellow)

    def add_office(self, new_office):
        # refactor office
        self.rooms['offices'][new_office.name] = new_office

    def add_livingspace(self, new_livingspace):
        # refactor settet livingspace
        self.rooms['livingspace'][new_livingspace.name] = new_livingspace

    def add_staff(self, new_staff):
        # refactor staff setter
        self.person['staff'][new_staff.id] = new_staff

    def add_fellow(self, new_fellow):
        # refactor fellow setter
        self.person['fellow'][new_fellow.id] = new_fellow

    def is_fellow(self, person):
        """
        returns true if person is fellow @ Dojo else False
        """
        return person.id in self.person['fellow']

    def is_staff(self, person):
        """
        returns True if person is staff @ Dojo else false
        """
        return person.id in self.person["staff"]

    def get_office(self, name):
        return self.rooms['offices'].get(name, False)

    def get_livingspace(self, name):
        return self.rooms['livingspace'].get(name, False)

    def get_person(self, person_id):
        staff = self.person['staff'].get(person_id, False)
        fellow = self.person['fellow'].get(person_id, False)
        person = staff if not fellow else fellow
        return person

    def get_person_room(self, person):
        results = [None, None]
        i = 0
        for room_type in self.rooms.keys():
            for room_name in self.rooms[room_type]:
                if self.rooms[room_type][room_name].is_in_room(person):
                    results[i] = self.rooms[room_type][room_name]
                    i += 1
                    break
        return results

    def remove_office(self, old_space):
        """
        Removes Office from the Dojo
        """
        if old_space.name in self.rooms['offices']:
            for occupants in old_space.occupants:
                occupants.office = False
            self.delete_from_db(old_space)
            del self.rooms['offices'][old_space.name]
            return True
        return False

    def remove_livingspace(self, old_space):
        """
        Removes LivingSpace from the Dojo
        """
        if old_space.name in self.rooms['livingspace']:
            for occupants in old_space.occupants:
                occupants.livingspace = False
            self.delete_from_db(old_space)
            del self.rooms['livingspace'][old_space.name]
            return True
        return False

    def remove_fellow(self, old_fellow):
        """
        Remove Fellow fro the Dojo
        Return True if succesfull else False
        """
        if old_fellow.id in self.person['fellow']:
            rooms = self.get_person_room(old_fellow)
            for room in rooms:
                if room:
                    room.occupants.remove(old_fellow)
            del self.person['fellow'][old_fellow.id]
            return True
        return False

    def remove_staff(self, old_staff):
        """
        Remove staff from the Dojo
        Return True if succesfull else False
        """
        if old_staff.id in self.person['staff']:
            rooms = self.get_person_room(old_staff)
            for room in rooms:
                if room:
                    room.occupants.remove(old_staff)
            self.delete_from_db(old_staff)
            del self.person['staff'][old_staff.id]
            return True
        return False

    def save_state(self, database_name="default.db", over_write=False, up=" "):
        if type(database_name) != str:
            raise TypeError
        if over_write:
            if os.path.exists("models/database/" + database_name):
                os.remove("models/database/" + database_name)
            raise OverWriteException
        if os.path.exists("models/database/" + database_name) and up:
            raise UpdateException

        if up:
            self.reset_db()

        self.init_db(database_name)
        self.database_session.add_all(list(self.fellow) + list(self.staff))
        self.database_session.add_all(list(self.office) +
                                      list(self.livingspace))
        self.database_session.commit()
        if not self.database_name:
            self.database_name = database_name

    def load_state(self, database_name="default.db", previous_state=False):
        if previous_state:
            database_name = "default.db"
        if type(database_name) != str:
            raise TypeError
        if not os.path.exists("models/database/" + database_name):
            raise DBDoesNotExistException

        # reset db
        self.reset_db()

        # initialize db
        self.init_db(database_name)

        # reset internal state
        self.rooms = {'offices': {}, 'livingspace': {}}
        self.person = {'fellow': {}, 'staff': {}}

        table_name = None
        key_value = None
        location_to_insert_item = None
        types_to_be_loaded = ['offices', 'livingspace', 'fellow', 'staff']
        for type_quried in types_to_be_loaded:
            if type_quried == 'offices' or type_quried == 'livingspace':
                table_name = Room
                key_value = "name"
                location_to_insert_item = self.rooms
            else:
                table_name = Person
                key_value = "id"
                location_to_insert_item = self.person
            data = self.query_database_table(table_name, type_quried)
            for item in data:
                value = None
                if key_value == "name":
                    value = item.name
                elif key_value == "id":
                    value = item.id
                location_to_insert_item[type_quried][value] = item

        # Update relevent variable
        Office.max_occupants = 6
        Office.number_of_offices += len(self.office)
        LivingSpace.max_occupants = 4
        LivingSpace.number_of_livingspace += len(self.livingspace)
        Person.number_of_person = len(self.staff) + len(self.fellow)

        self.loaded = True

    def init_db(self, database_name):
        if not self.database_engine:
            self.database_engine = load_engine(database_name)
        if self.db_migrations:
            create_tables(self.database_engine)
            self.db_migrations = False
        if not self.database_session:
            self.database_session = create_session(self.database_engine)

    def reset_db(self):
        if self.database_session:
            self.database_session.commit()
            self.database_session.close()
            self.database_session = None
        self.database_engine = None
        self.db_migrations = True

    def delete_from_db(self, item_in_db):
        if self.database_session:
            self.database_session.delete(item_in_db)
            self.database_session.commit()

    def query_database_table(self, table_name, type_quried):
        query_set = (self.database_session.query(table_name).filter_by
                     (type=type_quried))
        for item in query_set:
            yield item
