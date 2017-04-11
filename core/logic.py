from context import models
from models import model

dojo = None
def init_app():
    #create dojo
    if not dojo:
        return model.Dojo("Andela-Kenya")
    else:
        return dojo



def create_room(room_type, room_name):
    """
    input : room_type -> string represent type of room_type
    room_name -> string represent name of room_name
            output : returns -> return Room with name -> room_name
    Raises -> TypeError if room_name exists
            'Invalid name ' if room_name exists
    """
    #remove excess white charcters
    room_name_stripped =  room_name.strip()
    room_type_stripped = room_type.strip()

    if len(room_type_stripped) == 0:
        raise TypeError
    room_type_cleaned = room_type_stripped

    if len(room_name_stripped) == 0:
        return 'Invalid name'
    room_name_cleaned = room_name_stripped

    #map room_type to respective data type
    datatype = {'office' : model.Office, 'livingspace' : model.LivingSpace}

    if room_type_cleaned.lower() in datatype:
        return datatype[room_type_cleaned.lower()](room_name_cleaned)
    raise TypeError

def helper_create_and_addroom(room_type, room_name):
    status_messages = {'status': None, 'message' : None}
    new_room = create_room(room_type, room_name)

    if isinstance(new_room, model.Office):
        #add to Dojo Office
        dojo.office = new_room
        status_messages['status'] = 'ok'
        status_messages['message'] = "An office called {} has been successfully created!".format(new_room.name)
    elif isinstance(new_room, model.LivingSpace):
        #add to Dojo livingspace
        dojo.livingspace = new_room
        status_messages['status'] = 'ok'
        status_messages['message'] = "A LivingSpace called {} has been successfully created!".format(new_room.name)
    elif new_room == 'Invalid name':
        #give some status messge
        status_messages['status'] = 'Invalid name'
    else:
        status_messages['status'] = 'fail'

    return status_messages


def add_person():
    """
    input: firstname lastname Fellow/Staff [Y]
    """
    pass

def choose_office_random():
    pass

def choose_living_space_random():
    pass
