#room base
class Room():
    #keep track of all rooms created
    number_of_rooms = 0

    def __init__(self, max_occupants, name):
        '''
        return Room with no occupats
        '''
        self.__name = name
        self.__max_occupants = max_occupants
        self.occupants = []
        self.__id = Room.number_of_rooms
        Room.number_of_rooms += 1
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
        self.name = new_name
    @property
    def max_occupants(self):
        return self.__max_occupants

    def is_full(self):
        '''
        return True if room is full, else false
        '''
        return len(self.occupants) == Room.max_occupants
    def is_in_room(self, person):
        return person in self.occupants

    def add_occupant(self, person):
        if not self.is_in_room(person):
            self.occupants.append(person)
        #raise some error

    def remove_occupant(self, person):
        if self.is_in_room(person):
            del self.occupants[self.occupants.index(person)]
        #raise some error
    def get_occupants(self):
        occupants = self.occupants[:]
        def occupants():
            for person in occupants:
                yield person
        return occupants()



#create a Office
class Office(Room):
    max_occupants = 6
    number_of_offices = 0
    def __init__(self, name):
        Room.__init__(self, Office.max_occupants, name)
        Office.number_of_offices += 1

#create a LivingSpace
class LivingSpace(Room):
    max_occupants = 4
    number_of_livingspace = 0
    def __init__(self, name):
        Room.__init__(self, LivingSpace.max_occupants, name)
        LivingSpace.number_of_livingspace += 1
