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
    datatype = {'office' : model.Office, 'livingspace' : model.LivingSpace}
    if room_type.lower() in datatype:
        if room_name:
            return datatype[room_type.lower()](room_name)
        return 'Invalid name'
    raise TypeError
