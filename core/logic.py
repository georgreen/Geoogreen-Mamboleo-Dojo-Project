from context import models
from models import model


def create_room(room_type, room_name):
    """
    input : room_type -> string represent type of room_type
    room_name -> string represent name of room_name
            output : returns -> return Room with name -> room_name
    Raises -> TypeError if room_name exists
            'Invalid name ' if room_name exists
    """
    #remove excess white charcters
    room_name_stripped =  room_name.split()
    room_type_stripped = room_type.split()

    if len(room_type_stripped) == 0:
        raise TypeError
    room_type_cleaned = room_type_stripped[0]

    if len(room_name_stripped) == 0:
        return 'Invalid name'
    room_name_cleaned = room_name_stripped[0]

    #map room_type to respective data type
    datatype = {'office' : model.Office, 'livingspace' : model.LivingSpace}

    if room_type_cleaned.lower() in datatype:
        return datatype[room_type_cleaned.lower()](room_name_cleaned)
    raise TypeError

def add_person(*args):
    """
    input: firstname lastname Fellow/Staff [Y]
    """
    pass

def choose_office_random():
    pass

def choose_living_space_random():
    pass
