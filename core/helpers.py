import random

from models import model


def create_room(room_type, room_name, dojo):
    """
    input : room_type -> string represent type of room_type
    room_name -> string represent name of room_name
            output : returns -> return Room with name -> room_name
    Raises -> TypeError if room_name exists
            'Invalid name ' if room_name exists
    """
    # remove excess white charcters
    room_name_stripped = room_name.strip()
    room_type_stripped = room_type.strip()

    if len(room_type_stripped) == 0:
        raise TypeError
    room_type_cleaned = room_type_stripped

    if len(room_name_stripped) == 0 or not room_name_stripped.isalnum():
        return 'Invalid name'
    room_name_cleaned = room_name_stripped

    # map room_type to respective data type
    datatype = {'office': model.Office, 'livingspace': model.LivingSpace}

    if not room_type_cleaned.lower() in datatype:
        raise TypeError
    if room_name_cleaned in dojo.takken_names:
        return 'duplicates'
    return datatype[room_type_cleaned.lower()](room_name_cleaned)


def add_person(names, person_type, wants_livingspace='N'):
    """
    input: firstname lastname Fellow/Staff [Y]
    """

    # validate fields data types
    if not isinstance(names, tuple) or not isinstance(person_type, str) or\
            not isinstance(wants_livingspace, str):
        raise TypeError

    # validate person_type
    person_type = person_type.lower().strip()
    if person_type not in ["fellow", "staff"]:
        raise TypeError

    # validate name
    name1 = names[0].strip().lower()
    name2 = names[1].strip().lower()
    if not name1.isalnum() or not name2.isalnum():
        return "Invalid name"
    name = name1 + " " + name2

    # validate wants_livingspace
    wants_livingspace = wants_livingspace.strip().lower()
    if wants_livingspace not in 'yn' and person_type == "fellow":
        return "Invalid choice"
    choice = True if wants_livingspace == 'y' else False

    if person_type == 'staff':
        new_person = model.Staff(name)
        new_person.office = False
    else:
        new_person = model.Fellow(name, choice)
        new_person.livingspace = False
        new_person.office = False
        new_person.wants_living = False
        if choice:
            new_person.wants_living = True
    return new_person


def allocate_room(new_person, dojo):
    """
    allocates a room to new_person
    Returns a dictionary of status messages about success of adding to rooms
    """
    status_messages = {'office': None, 'livingspace': None}

    if new_person == 'Invalid name':
        status_messages['status'] = 'Invalid name'
        return status_messages
    elif new_person == "Invalid choice":
        status_messages['status'] = 'Invalid choice'
        return status_messages
    elif isinstance(new_person, model.Fellow):
        if new_person.wants_living:
            status_messages['livingspace'] = allocate_livingspace(new_person,
                                                                  dojo=dojo)
        dojo.add_fellow(new_person)
        status_messages['person_type'] = 'fellow'
    else:
        dojo.add_staff(new_person)
        status_messages['person_type'] = 'staff'
    status_messages['office'] = allocate_office(new_person, dojo=dojo)

    return status_messages


def allocate_office(new_person, dojo, name_office=None):
    '''
    allocates office to new person_type
    Returns name of office if added else None
    '''
    if not name_office:
        name_office = choose_office_random(dojo)

    office = dojo.get_office(name_office)
    if name_office != "NoRoomException" and not office.is_full():
        dojo.add_person_office(name_office, new_person)
        new_person.office = True
        name_office = office.name
    else:
        name_office = None

    return name_office


def allocate_livingspace(new_person, dojo, name_livingspace=None):
    '''
    allocates livingspace to new_person
    Returns name of living space if added else None
    '''
    if not name_livingspace:
        name_livingspace = choose_living_space_random(dojo)

    livingspace = dojo.get_livingspace(name_livingspace)
    if name_livingspace == "NoRoomException" or livingspace.is_full():
        name_livingspace = None
    elif new_person.wants_living:
        dojo.add_fellow_living(name_livingspace, new_person)
        new_person.livingspace = True
        name_livingspace = livingspace.name
    else:
        name_livingspace = None

    return name_livingspace


def choose_office_random(dojo):
    """
    choose an office at random
    """
    number_of_offices = len(dojo.office)
    if number_of_offices > 0:
        index = random.randrange(number_of_offices)
    else:
        return "NoRoomException"
    list_offices = list(dojo.office)
    return list_offices[index].name


def choose_living_space_random(dojo):
    """
    choose a livingspace at random
    """
    number_of_livingspace = len(dojo.livingspace)
    if number_of_livingspace > 0:
        index = random.randrange(number_of_livingspace)
    else:
        return "NoRoomException"
    list_livingspace = list(dojo.livingspace)
    return list_livingspace[index].name


class NoRoomException(Exception):
    pass


def save_data_text(file_name, data, mode='wt'):
    if file_name[len(file_name) - 4:] != '.txt':
        file_name = file_name + '.txt'

    file_out = open(file_name, mode)
    for name in data:
        print(name, file=file_out)
    file_out.close()


def load_data_text(file_name):
    data = []
    raw_data = open(file_name, 'rt')
    while True:
        line = raw_data.readline()
        if not line:
            break
        data.append(line.split())
    return data


def deallocate_person(room_type, person, office=None, livingspace=None):
    deallocation = None
    if room_type == 'O' and office:
        deallocation = deallocate_office(person, office)
    elif room_type == 'L' and livingspace:
        deallocation = deallocate_livingspace(person, livingspace)
    elif room_type == 'L' and isinstance(person, model.Staff):
        deallocation = 'Invalid Operation'

    return deallocation


def get_roomname_type(room_name, dojo):
    status_messages = {}
    room_name = room_name.strip().lower()
    if room_name not in dojo.takken_names:
        status_messages['status'] = "Room not found"
    else:
        office = dojo.get_office(room_name.strip().lower())
        livingspace = dojo.get_livingspace(room_name.strip().lower())

        # we can only reallocate one room at a time office or livingspace
        status_messages['in'] = (office, 'O') if office else (livingspace, 'L')
        status_messages['status'] = 'ok'
    return status_messages


def deallocate_livingspace(person, room):
    if isinstance(person, model.Staff):
        return 'Invalid Operation'
    if person.is_allocated_living() and person.wants_living:
        room.remove_occupant(person)
        person.livingspace = False
    elif not person.wants_living:
        return 'Invalid Operation'
    return 'Done'


def deallocate_office(person, room):
    room.remove_occupant(person)
    person.office = False
    return 'Done'
