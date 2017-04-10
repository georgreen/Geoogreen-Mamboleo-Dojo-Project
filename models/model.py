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
        self.__name = name
        self.__max_occupants = max_occupants
        self.__occupants = []
        self.__id = Room.number_of_rooms
        Room.number_of_rooms += 1

    @property
    def id(self):
        return __id
        
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
        Room.__init__(self, Office.max_occupants, name)
        Office.number_of_offices += 1

#create a LivingSpace
class LivingSpace(Room):
    #number of LivingSpaces
    number_of_livingspace = 0

    max_occupants = 4
    def __init__(self, name):
        Room.__init__(self, LivingSpace.max_occupants, name)
        LivingSpace.number_of_livingspace += 1
