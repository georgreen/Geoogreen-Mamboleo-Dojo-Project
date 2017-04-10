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
        self.__name = name
        self.__max_occupants = max_occupants
        self.__occupants = []
        self.__id = Room.number_of_rooms


    @property
    def id(self):
        '''
        return id, unique identifier for room
        '''
        return self.__id

    @property
    def name(self):
        '''
        property name, return name for room
        '''
        return self.__name

    @name.setter
    def name(self, new_name):
        '''
        setter: set's name for room
        '''
        self.__name = new_name

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
        return len(self.__occupants) == Room.max_occupants

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
    #number of offices a
    number_of_offices = 0

    max_occupants = 6
    def __init__(self, name):
        Office.number_of_offices += 1
        Room.__init__(self, Office.max_occupants, name)


#create a LivingSpace
class LivingSpace(Room):
    #number of LivingSpaces
    number_of_livingspace = 0

    max_occupants = 4
    def __init__(self, name):
        LivingSpace.number_of_livingspace += 1
        Room.__init__(self, LivingSpace.max_occupants, name)



################################################################################
class Person():
    #number of Person
    number_of_person = 0

    def __init__(self, name):
        Person.number_of_person += 1
        self.__id = Person.number_of_person
        self.__name = name
        self.__office = None


    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def id(self):
        return self.__id

    @property
    def office(self):
        return self.__office

    @office.setter
    def office(self, office):
        self.__office = office

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
        self.__wants_living = wants_living
        self.__livingspace = None


    def is_allocated_living(self):
        return not not self.__livingspace

    @property
    def wants_living(self):
        return self.__wants_living
    @property
    def livingspace(self):
        return self.__livingspace
    @livingspace.setter
    def livingspace(self, space):
        if self.__wants_living:
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
