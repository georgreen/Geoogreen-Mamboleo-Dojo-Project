# model a room
from models.base_db import (Base, Column, ForeignKey, Integer, String,
                            relationship)


class Room(Base):
    '''
    models abstract data type Room, not intended to be instanciated
    '''
    __tablename__ = 'rooms'

    number_of_rooms = Column(Integer, default=0)
    name = Column(String(256))
    type = Column(String(50))
    id = Column(Integer, primary_key=True)
    occupants = relationship('Person')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'rooms'
    }

    def __init__(self, max_occupants, name):
        '''
        return Room with no occupats
        '''
        Room.number_of_rooms += 1
        self.name = name
        self.max_occupants = max_occupants
        self.occupants = []
        self.__id = Room.number_of_rooms

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

    def is_in_room(self, user):
        '''
        returns true if user in room_name
        '''
        return user in self.occupants

    def add_occupant(self, user):
        '''
        adds user to room_name
        '''
        self.occupants.append(user)

    def remove_occupant(self, user):
        '''
        removes user from room
        '''
        if self.is_in_room(user):
            del self.occupants[self.occupants.index(user)]
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

    __mapper_args__ = {
        'polymorphic_identity': 'offices'
    }

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

    __mapper_args__ = {
        'polymorphic_identity': 'livingspace'
    }

    def __init__(self, name):
        LivingSpace.number_of_livingspace += 1
        Room.__init__(self, LivingSpace.max_occupants, name)
