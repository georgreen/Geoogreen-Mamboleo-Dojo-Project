from models import model
from core import helpers


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

    if len(room_name_stripped) == 0:
        return 'Invalid name'
    room_name_cleaned = room_name_stripped

    # map room_type to respective data type
    datatype = {'office': model.Office, 'livingspace': model.LivingSpace}

    if not room_type_cleaned.lower() in datatype:
        raise TypeError
    if room_name_cleaned in dojo.takken_names:
        return 'duplicates'
    return datatype[room_type_cleaned.lower()](room_name_cleaned)


def helper_create_and_addroom(dojo, room_type, room_name):
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
    if wants_livingspace not in 'yn':
        return "Invalid choice"
    choice = True if wants_livingspace == 'y' else False

    if person_type == 'staff':
        new_person = model.Staff(name)
        new_person.office = False
    else:
        new_person = model.Fellow(name, choice)
        new_person.livingspace = False
        new_person.office = False
    return new_person


def helper_addsperson_chooseroom(dojo, first_name, second_name, person_type, choice_live='N'):
    """
    add a person to dojo and allocates office and [livingspace]
    """
    status_messages = {'status': None, 'message': []}
    if not choice_live:
        choice_live = 'N'
    try:
        new_person = add_person((first_name, second_name), person_type, choice_live)
        status_messages['status'] = 'ok'
        new_person.office = None
        msg = "{} {} {} has been successfully added.".format(person_type, first_name, second_name)
        status_messages['message'].append(msg)
    except TypeError:
        status_messages['status'] = 'Failed'
        msg = "{} {} {} has not added.".format(person_type, first_name, second_name)
        status_messages['message'].append(msg)
        return status_messages

    return allocate_room(new_person, dojo, status_messages)


def allocate_room(new_person, dojo, status_messages):
    """
    allocates a room to new_person
    """

    # status_messages = {'status': 'ok', 'message': []}
    if isinstance(new_person, model.Staff):
        # add to dojo
        dojo.add_staff(new_person)
        name_office = helpers.choose_office_random(dojo)
        if name_office != "NoRoomException" and \
                not dojo.get_office(name_office).is_full():

            dojo.add_person_office(name_office, new_person)
            office = dojo.get_office(name_office)
            new_person.office = True
            msg = "{} has been allocated the office {}".format(new_person.name, office.name)
            status_messages['message'].append(msg)
        else:
            # change status to not added no room
            msg = "{} not has been allocated the office".format(new_person.name)
            status_messages['message'].append(msg)
    elif isinstance(new_person, model.Fellow):
        # add to dojo
        dojo.add_fellow(new_person)

        # generate random names for rooms
        name_livingspace = helpers.choose_living_space_random(dojo)
        name_office = helpers.choose_office_random(dojo)

        # assign fellow office
        if name_office != "NoRoomException" and \
           not dojo.get_office(name_office).is_full():

            dojo.add_person_office(name_office, new_person)
            office = dojo.get_office(name_office)
            new_person.office = True
            msg = "{} has been allocated the office {}".format(new_person.name, office.name)
            status_messages['message'].append(msg)
        else:
            msg = "{} has not been allocated an office".format(new_person.name)
            status_messages['message'].append(msg)

        # assign fellow living space
        if name_livingspace == "NoRoomException" or \
                dojo.get_livingspace(name_livingspace).is_full():

            msg = "{} not has been allocated a livingspace".format(new_person.name)
            status_messages['message'].append(msg)
        elif new_person.wants_living:
            dojo.add_fellow_living(name_livingspace, new_person)
            livingspace = dojo.get_livingspace(name_livingspace)
            new_person.livingspace = True
            msg = "{} has been allocated the livingspace {} ".format(new_person.name, livingspace.name)
            status_messages['message'].append(msg)
    elif new_person == 'Invalid name':
        status_messages['status'] = 'Invalid name'
        msg = "{} {} has not been  added  ".format(person_type, name)
        status_messages['message'] = []
    elif new_person == "Invalid choice":
        status_messages['status'] = 'Invalid choice'
        msg = "{} {} has not been  added  ".format(person_type, name)
        msg_not_allocated = "{} {} has not been  allocated living space  ".format(person_type, name)
        status_messages['message'] = [msg]

    return status_messages


def people_inroom(dojo, room_name):
    """
    returns the names of all the people in room_name
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
    returns a dict of allocations
    if file_name is specified values are saved txt
    """
    allocations = {}
    rooms = list(dojo.office) + list(dojo.livingspace)
    for room in rooms:
        allocations[room.name] = people_inroom(dojo, room.name)

    return allocations


def list_unallocated(dojo, file_name=''):
    """
    returns a list of unallocated people to the screen
    if file_name is specified values are saved txt
    """
    unallocated = []
    person = dojo.person

    # go over fellow first
    for fellow in person['fellow'].values():
        if (not fellow.is_allocated_living()) or (not fellow.is_allocated_office()):
            unallocated.append(fellow)
    # go over staff
    for staff in person['staff'].values():
        if not staff.is_allocated_office():
            unallocated.append(staff)
    return unallocated


def save_data_txt(file_name, raw_data, mode='wt'):
    helpers.save_data_txt(file_name, raw_data, mode)


def load_data_txt(file_name, dojo):
    status_data = []
    try:
        loaded_data = helpers.load_data_txt(file_name)
    except FileNotFoundError:
        return {'status': 'failed', 'message': 'File Not Found Error'}
    for user_info in loaded_data:
        if len(user_info) > 2 and len(user_info) < 5:
            first_name, second_name, person_type = user_info[:3]
            choice_live = 'N'
            if len(user_info) == 4:
                choice_live = user_info[3]
            status = helper_addsperson_chooseroom(dojo, first_name, second_name, person_type, choice_live)
            status_data.append(status)
        else:
            msg = {'status': 'failed', 'message': ' '.join(user_info) + ": was not Added, Invalid format"}
            status_data.append(msg)
    return status_data


def reallocate_person(room_name, person_id, dojo):
    find_person = None
    find_room = None
    current_rooms = None

    try:
        person_id = int(person_id)
    except ValueError:
        return "Invalid  User Id"

    # get the person
    find_person = dojo.get_person(person_id)

    if not find_person or person_id < 0:
        return "Person not found"

    # get the room
    room_name = room_name.strip().lower()
    current_livingspace = None
    current_office = None
    if room_name not in dojo.takken_names:
        return "Room not found"
    else:
        office = dojo.get_office(room_name.strip().lower())
        livingspace = dojo.get_livingspace(room_name.strip().lower())

        # we can only reallocate one room at a time
        find_room = office if office else livingspace

        # find all current rooms allocated to person
        current_rooms = dojo.get_person_room(find_person)
        for room in current_rooms:
            if isinstance(room, model.Office):
                current_office = room
            elif isinstance(room, model.LivingSpace):
                current_livingspace = room

    # handle deallocating fellow from livingspaces
    # contain current room from current rooms
    current_room = None
    if isinstance(find_person, model.Fellow):
        if isinstance(find_room, model.LivingSpace):
            # check to see if fellow what's living space
            if not find_person.wants_living:
                return "Invalid Operation don't want living space"
            # switch current room to living space
            current_room = current_livingspace

            # remove them in previoius room
            if find_person.is_allocated_living():
                current_room.remove_occupant(find_person)
            # allocate to new room
            if not find_room.is_full():
                find_room.add_occupant(find_person)
                find_person.livingspace = True
                return "successfully added to livingspace"
            else:
                return "Room full"

        else:
            # switch current room to office
            current_room = current_office

    # staff not allowed to have living space
    if isinstance(find_person, model.Staff):
        # return invalid if current room is None
        if not current_room:
            return "Invalid operations"

    # handle office deallocation both staff and fellow
    if isinstance(find_room, model.Office):
        if current_room:
            current_room.remove_occupant(find_person)
        if not find_room.is_full():
            find_room.add_occupant(find_person)
            find_person.office = True
            return "Succesfully added to Office"
        else:
            return "Room full"
    return 'Error rellocation failed'
