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
