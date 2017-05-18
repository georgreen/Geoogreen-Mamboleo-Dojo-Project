from core import helpers
from core.helpers import *
from models import model


def create_and_addroom(dojo, room_type, room_name):
    '''
    uses create room to create a room
    adds's new room to dojo, if valid
    '''
    status_messages = {}
    status_messages['status'] = None
    status_messages['room_name'] = room_name
    status_messages['room_type'] = room_type
    new_room = None
    try:
        new_room = create_room(room_type, room_name, dojo)
    except TypeError:
        status_messages['status'] = 'failed'

    if new_room == 'duplicates':
        status_messages['status'] = 'Duplicate name'
    elif new_room == 'Invalid name':
        status_messages['status'] = 'Invalid name'
    elif isinstance(new_room, model.Office):
        dojo.add_office(new_room)
        status_messages['status'] = 'ok'
    elif isinstance(new_room, model.LivingSpace):
        dojo.add_livingspace(new_room)
        status_messages['status'] = 'ok'
    return status_messages


def addsperson_chooseroom(dojo, first_name, second_name, person_type, choice_live='N'):
    """
    add a person to dojo and allocates office and [livingspace]
    """
    # set up status message respond
    status_messages = {'status': None, 'person_type': person_type}
    status_messages['name'] = first_name + ' ' + second_name
    status_messages['id'] = None

    choice = 'Y'
    if not choice_live or choice_live.lower() not in 'y':
        choice = 'N'
        choice_live = False
    else:
        choice_live = True
    status_messages['choice_live'] = choice_live

    try:
        new_person = add_person((first_name, second_name), person_type, choice)
        status_messages['status'] = 'ok'
        status_messages['id'] = new_person.id
        new_person.office = None
    except TypeError:
        status_messages['status'] = 'Failed'
        return status_messages

    room_update = allocate_room(new_person, dojo)
    status_messages.update(room_update)
    return status_messages


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
            status_messages['livingspace'] = allocate_livingspace(new_person, dojo=dojo)
        dojo.add_fellow(new_person)
        status_messages['person_type'] = 'fellow'
    else:
        dojo.add_staff(new_person)
        status_messages['person_type'] = 'staff'
    status_messages['office'] = allocate_office(new_person, dojo=dojo)

    return status_messages


def people_inroom(dojo, room_name):
    """
    input: room_name and dojo
    returns: the names of all the people in room_name
    """
    room_name = room_name.strip()
    rooms = list(dojo.office) + list(dojo.livingspace)
    for room in rooms:
        if room.name == room_name:
            return list(room.get_occupants())
    raise NotFoundException


class NotFoundException(Exception):
    pass


def dict_allocations(dojo):
    """
    input: dojo
    returns a dict of allocations
    """
    allocations = {}
    rooms = list(dojo.office) + list(dojo.livingspace)
    for room in rooms:
        allocations[room.name] = people_inroom(dojo, room.name)

    return allocations


def list_unallocated(dojo, file_name=''):
    """
    input: dojo & [file_name]
    returns a list of unallocated people to the screen
    if file_name is specified values are saved to file_name.txt
    """
    unallocated = []
    person = dojo.person

    # go over fellow first
    for fellow in person['fellow'].values():
        allocated_living = fellow.is_allocated_living()
        allocated_office = fellow.is_allocated_office()
        if not allocated_office or (not allocated_living and fellow.wants_living):
            unallocated.append(fellow)

    # go over staff
    for staff in person['staff'].values():
        if not staff.is_allocated_office():
            unallocated.append(staff)
    return unallocated


def save_txt(file_name, raw_data, mode='wt'):
    save_data_txt(file_name, raw_data, mode)


def load_data_txt(file_name, dojo):
    status_data = []
    try:
        if file_name[len(file_name) - 4:] == '.txt':
            loaded_data = helpers.load_data_txt(file_name)
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        return [{'status': 'filenotfound', 'message': 'File Not Found'}]
    for user_info in loaded_data:
        if len(user_info) > 2 and len(user_info) < 5:
            first_name, second_name, person_type = user_info[:3]
            choice_live = 'N'
            if len(user_info) == 4:
                choice_live = user_info[3]
            status = addsperson_chooseroom(dojo, first_name, second_name, person_type, choice_live)
            status_data.append(status)
        elif len(user_info) > 0:
            msg = {'status': 'illegalformat', 'message': ' '.join(user_info) + ": was not Added."}
            status_data.append(msg)
    return status_data


def reallocate_person(room_name, person_id, dojo):

    person = room = None
    status_messages = {'status': 'Fail'}
    try:
        person_id = int(person_id)
    except ValueError:
        status_messages['message'] = "Invalid  User Id"
        return status_messages

    # get the person to be moved
    person = dojo.get_person(person_id)
    if not person or person_id < 0:
        status_messages['message'] = "Person not found"
        return status_messages

    # get the room to be reallocated to
    room_type = None
    room_info = get_roomname_type(room_name, dojo)
    if room_info['status'] != 'ok':
        status_messages['message'] = "Room not found"
        return status_messages
    else:
        room_name, room_type = room_info['in']
        status_messages['current_room'] = room_name.name

    # find all current rooms allocated to person
    current_rooms = dojo.get_person_room(person)
    current_livingspace = current_office = None
    for room in current_rooms:
        if isinstance(room, model.Office):
            current_office = room
        elif isinstance(room, model.LivingSpace):
            current_livingspace = room
    status_messages['prev_office'] = current_office
    status_messages['prev_livingspace'] = current_livingspace

    deallocation = deallocate_person(room_type, person, current_office, current_livingspace)
    status_messages['deallocation'] = deallocation
    status_messages['name'] = person.name
    status_messages['room_type'] = room_type

    if deallocation != 'Invalid Operation':
        name = room_name.name
        status_messages['status'] = 'ok'
        msg = None
        if room_type == 'O':
            msg = allocate_office(person, name_office=name, dojo=dojo)
        elif person.wants_living:
            msg = allocate_livingspace(person, name_livingspace=name, dojo=dojo)
            status_messages['choice'] = person.wants_living
        if not msg:
            status_messages['status'] = 'Invalid Operation'
    else:
        status_messages['status'] = 'Invalid Operation'

    return status_messages


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
