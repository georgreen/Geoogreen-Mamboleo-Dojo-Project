#room base
class Room():
    '''
    models abstract data type Room, not intended to be instanciated
    '''
    #keep track of all rooms created
    number_of_rooms = 0

    def __init__(self, max_occupants, name):
        '''
        return Room with no occupats
        '''
        Room.number_of_rooms += 1
        self.name = name
        self.__max_occupants = max_occupants
        self.__occupants = []
        self.__id = Room.number_of_rooms

    @property
    def max_occupants(self):
        return self.__max_occupants

    @property
    def current_population(self):
        '''
        return number of ppl in room
        '''
        return len(self.__occupants)

    def is_full(self):
        '''
        return True if room is full, else false
        '''
        return len(self.__occupants) == self.max_occupants

    def is_in_room(self, person):
        '''
        returns true if person in room_name
        '''
        return person in self.__occupants

    def add_occupant(self, person):
        '''
        adds person to room_name
        '''
        if self.current_population == self.max_occupants:
            pass
            #raise full error
        if not self.is_in_room(person):
            self.__occupants.append(person)

        #raise some error

    def remove_occupant(self, person):
        '''
        removes person from room
        '''
        if self.is_in_room(person):
            del self.__occupants[self.__occupants.index(person)]
        #raise some error
    def get_occupants(self):
        '''
        returns a generator with all occupants
        '''
        occupants = self.__occupants[:]
        def occupants():
            for person in occupants:
                yield person
        return occupants()



#create a Office
class Office(Room):
    """
    input name -> string
    models Offices space
    """
    #number of offices a
    number_of_offices = 0

    max_occupants = 6
    def __init__(self, name):
        Office.number_of_offices += 1
        Room.__init__(self, Office.max_occupants, name)


#create a LivingSpace
class LivingSpace(Room):
    """
    input : name -> string
    models a LivingSpace
    """
    #number of LivingSpaces
    number_of_livingspace = 0

    max_occupants = 4
    def __init__(self, name):
        LivingSpace.number_of_livingspace += 1
        Room.__init__(self, LivingSpace.max_occupants, name)


################################################################################
class Dojo():
    """
    input name -> string
    models Dojo facillity
    """
    facillity_names = []
    def __init__(self, name):
        if type(name) != type("str"):
            raise TypeError

        if name in Dojo.facillity_names:
            raise DuplicateError

        self.__cleaned_name = self.clean_name(name)

        if not self.__cleaned_name:
            raise TypeError


        self.__number_rooms = 0
        self.__number_office = 0
        self.__number_livingspace = 0
        self.__rooms = {'offices' : [], 'livingspace' : []}
        self.__person = {'fellow' : [], 'staff' : []}
        self.name = self.__cleaned_name
        Dojo.facillity_names.append(self.__cleaned_name)

    #validate name
    def clean_name(self, name):
        clean_name = ''
        name_stripped = name.split()
        if len(name_stripped) == 0:
            return ''

        cleaned_name = name_stripped[0]

        #check for atleat one letter

        if cleaned_name:
            return cleaned_name

    @property
    def room(self, room):
        """
        returns a copy  all rooms
        """
        return self.__rooms['offices'] + self.__rooms['livingspace']


    @property
    def office(self):
        """
        returns a copy of all offices
        """
        return self.__rooms['offices'][:]
    @office.setter
    def office(self, new_office):
        """
        Adds new office to dojo
        """
        self.__rooms['offices'].append(new_office)
    @property
    def livingspace(self):
        """
        returns a copy of all the lving space
        """

        return self.__rooms['livingspace'][:]
    @livingspace.setter
    def livingspace(self, new_livingspace):
        """
        Adds new livingspace to the dojo
        """
        self.__rooms['livingspace'].append(new_livingspace)

    @property
    def fellow(self):
        """
        returns a copy of all fellows
        """
        return self.__person['fellow'][:]
    @fellow.setter
    def fellow(self, new_fellow):
        """
        Adds a new fellow to dojo
        """
        self.__person['fellow'].append(new_fellow)
    def is_fellow(self, person):
        """
        returns true if person is fellow @ Dojo else False
        """
        return person in self.__person['fellow']

    @property
    def staff(self):
        """
        returns a copy of the staff
        """
        return self.__person['staff'][:]
    @staff.setter
    def staff(self, new_staff):
        """
        Adds new staff to the Dojo
        """
        self.__person['staff'].append(new_staff)
    def is_staff(self, person):
        """
        returns True if person is staff @ Dojo else false
        """
        return person in self.__person["staff"]

    def remove_office(self, old_space):
        """
        Removes Office from the Dojo
        """
        if old_space in self.__rooms['offices']:
            del self.__rooms['offices'][self.__rooms['offices'].index(old_space)]

    def remove_livingspace(self, old_space):
        """
        Removes LivingSpace from the Dojo
        """
        if old_space in self.__rooms['livingspace']:
            del self.__rooms['livingspace'][self.__rooms['livingspace'].index(old_space)]

    def remove_fellow(self, old_fellow):
        """
        Remove Fellow fro the Dojo
        """
        if old_fellow in self.__person['fellow']:
            del self.__person['fellow'][self.__person['fellow'].index(old_fellow)]
    def remove_staff(self, old_staff):
        """
        Remove staff from the Dojo
        """
        if old_staff in self.__person['staff']:
            del self.__person['staff'][self.__person['staff'].index(old_staff)]

#exception throw for duplicates insertions
class DuplicateError(Exception):
    pass




################################################################################
class Person():
    #number of Person
    number_of_person = 0

    def __init__(self, name):
        Person.number_of_person += 1
        self.__id = Person.number_of_person
        self.__name = name
        self.office = None

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def id(self):
        return self.__id

    def remove_office(self):
        self.office = None

    def is_allocated_office(self):
        return not (not self.office)



class Fellow(Person):
    #number of fellows
    number_of_fellows = 0

    def __init__(self, name, wants_living = False):
        Fellow.number_of_fellows += 1
        Person.__init__(self, name)
        self.wants_living = wants_living
        self.__livingspace = None


    def is_allocated_living(self):
        return not not self.__livingspace

    @property
    def livingspace(self):
        return self.__livingspace
    @livingspace.setter
    def livingspace(self, space):
        if self.wants_living:
            self.__livingspace = space
        #throw value error
    def remove_livingspace(self):
        self.__livingspace = None

class Staff(Person):
    #number of Staff
    number_of_staff = 0
    def __init__(self, name):
        Staff.number_of_staff += 1
        Person.__init__(self, name)
