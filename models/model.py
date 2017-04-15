# model a room
class Room():
    '''
    models abstract data type Room, not intended to be instanciated
    '''
    # keep track of all rooms created
    number_of_rooms = 0
    takken_names = []

    def __init__(self, max_occupants, name):
        '''
        return Room with no occupats
        '''
        Room.number_of_rooms += 1
        self.name = name
        self.max_occupants = max_occupants
        self.occupants = []
        self.__id = Room.number_of_rooms
        Room.takken_names.append(name)

    @property
    def current_population(self):
        '''
        return number of ppl in room
        '''
        return len(self.occupants)

    def is_full(self):
        '''
        return True if room is full, else false
        '''
        return self.current_population == self.max_occupants

    def is_in_room(self, person):
        '''
        returns true if person in room_name
        '''
        return person in self.occupants

    def add_occupant(self, person):
        '''
        adds person to room_name
        '''
        self.occupants.append(person)

    def remove_occupant(self, person):
        '''
        removes person from room
        '''
        if self.is_in_room(person):
            del self.occupants[self.occupants.index(person)]
            return True
        return False

    def get_occupants(self):
        '''
        returns a generator with all occupants
        '''
        return self.occupants


# model a Office
class Office(Room):
    """
    input name -> string
    models Offices space
    """
    # number of offices a
    number_of_offices = 0
    max_occupants = 6

    def __init__(self, name):
        Office.number_of_offices += 1
        Room.__init__(self, Office.max_occupants, name)


# model a LivingSpace
class LivingSpace(Room):
    """
    input : name -> string
    models a LivingSpace
    """
    # number of LivingSpaces
    number_of_livingspace = 0
    max_occupants = 4

    def __init__(self, name):
        LivingSpace.number_of_livingspace += 1
        Room.__init__(self, LivingSpace.max_occupants, name)


###########################################################################
class Dojo():
    """
    input name -> string
    models Dojo facillity
    """
    facillity_names = []

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError
        if name in Dojo.facillity_names:
            raise DuplicateError
        self.__cleaned_name = Dojo.clean_name(name)
        if not self.__cleaned_name:
            raise TypeError

        self.__number_livingspace = 0
        self.__number_offices = 0
        self.rooms = {'offices': {}, 'livingspace': {}}
        self.person = {'fellow': {}, 'staff': {}}
        self.name = self.__cleaned_name
        self.office = self.rooms['offices'].values()
        self.livingspace = self.rooms['livingspace'].values()
        self.fellow = self.person['fellow'].values()
        self.staff = self.person['staff'].values()
        self.takken_names = set()
        Dojo.facillity_names.append(self.__cleaned_name)

    # validate name
    def clean_name(name):
        clean_name = ""
        name_stripped = name.split()
        if len(name_stripped) == 0:
            return ''
        cleaned_name = name_stripped[0]
        # check for atleat one letter
        if cleaned_name:
            return cleaned_name

    def add_person_office(self, name, staff):
        self.rooms['offices'][name].add_occupant(staff)

    def add_fellow_living(self, name, fellow):
        self.rooms['livingspace'][name].add_occupant(fellow)

    def add_office(self, new_office):
        # refactor office
        self.rooms['offices'][new_office.name] = new_office
        self.takken_names.add(new_office.name)

    def add_livingspace(self, new_livingspace):
        # refactor settet livingspace
        self.rooms['livingspace'][new_livingspace.name] = new_livingspace
        self.takken_names.add(new_livingspace.name)

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
            del self.rooms['offices'][old_space.name]
            return True
        return False

    def remove_livingspace(self, old_space):
        """
        Removes LivingSpace from the Dojo
        """
        if old_space.name in self.rooms['livingspace']:
            del self.rooms['livingspace'][old_space.name]
            return True
        return False

    def remove_fellow(self, old_fellow):
        """
        Remove Fellow fro the Dojo
        Return True if succesfull else False
        """
        if old_fellow.id in self.person['fellow']:
            del self.person['fellow'][old_fellow.id]
            return True
        return False

    def remove_staff(self, old_staff):
        """
        Remove staff from the Dojo
        Return True if succesfull else False
        """
        if old_staff.id in self.person['staff']:
            del self.person['staff'][old_staff.id]
            return True
        return False


# exception throw for duplicates insertions
class DuplicateError(Exception):
    pass


####################################################################
class Person():
    # number of Person
    number_of_person = 0

    def __init__(self, name):
        Person.number_of_person += 1
        self.__id = Person.number_of_person
        self.name = name
        self.office = None

    @property
    def id(self):
        '''
        person's Id based off number of ppl created
        '''
        return self.__id

    def remove_office(self):
        self.office = None

    def is_allocated_office(self):
        return not (not self.office)


class Fellow(Person):
    # number of fellows
    number_of_fellows = 0

    def __init__(self, name, wants_living=False):
        Fellow.number_of_fellows += 1
        Person.__init__(self, name)
        self.wants_living = wants_living
        self.livingspace = False

    def is_allocated_living(self):
        return self.livingspace

    def set_livingspace(self, space):
        if self.wants_living:
            pass

    def remove_livingspace(self):
        self.livingspace = None


class Staff(Person):
    # number of Staff
    number_of_staff = 0

    def __init__(self, name):
        Staff.number_of_staff += 1
        Person.__init__(self, name)
