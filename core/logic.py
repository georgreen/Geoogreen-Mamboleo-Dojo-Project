from context import models
from models import model
import random


def create_room(room_type, room_name, dojo):
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
    status_messages = {'status': None, 'message' : None}
    new_room = create_room(room_type, room_name, dojo)

    if isinstance(new_room, model.Office):
        #add to Dojo Office
        dojo.add_office(new_room)
        status_messages['status'] = 'ok'
        status_messages['message'] = "An office called {} has been successfully created!".format(new_room.name)
    elif isinstance(new_room, model.LivingSpace):
        #add to Dojo livingspace
        dojo.add_livingspace(new_room)
        status_messages['status'] = 'ok'
        status_messages['message'] = "A LivingSpace called {} has been successfully created!".format(new_room.name)
    elif new_room == 'duplicates':
        #give some status messge
        status_messages['status'] = 'Invalid name'
        status_messages['message'] = "{} called {} can not be created!: Name already exists".format(room_type, room_name)
    else:
        status_messages['status'] = 'Invalid name'
        status_messages['message'] = "{} called {} can not be created!:ERROR".format(room_type, room_name)

    return status_messages


def add_person(names, person_type, wants_livingspace = 'N'):
    """
    input: firstname lastname Fellow/Staff [Y]
    """
    #validate fields data types
    if type(names) != tuple or type(person_type) != str or type(wants_livingspace) != str:
        raise TypeError

    #validate person_type
    person_type = person_type.lower().strip()

    if person_type not in ["fellow", "staff"]:
        raise TypeError

    #validate name
    name1 = names[0].strip().lower()
    name2 = names[1].strip().lower()
    if not name1.isalnum() or not name2.isalnum():
        return "Invalid name"
    name = name1 + " " + name2
    #validate wants_livingspace
    wants_livingspace = wants_livingspace.strip().lower()
    if wants_livingspace not in 'yn':
        return "Invalid choice"
    choice = False
    if wants_livingspace == 'y':
        choice = True

    if person_type == 'staff':
        return model.Staff(name)
    return model.Fellow(name, choice)


def choose_office_random(dojo):
    """
    choose an office at random
    """
    number_of_offices = len(dojo.office)
    if number_of_offices > 0:
        index = random.randrange(number_of_offices)
    else:
        return "NoRoomException"
    return index

def choose_living_space_random(dojo):
    """
    choose a livingspace at random
    """
    number_of_livingspace = len(dojo.livingspace)
    if number_of_livingspace > 0:
        index = random.randrange(number_of_livingspace)
    else:
        return "NoRoomException"
    return index

class NoRoomException(Exception):
    pass

def helper_addsperson_chooseroom(dojo, first_name, second_name, person_type, choice_live = 'N'):
    """
    add a person to dojo and allocates office and [livingspace]
    """
    status_messages = {'status': None, 'message' : []}
    if not choice_live :
        choice_live = 'N'
    try:
        new_person = add_person((first_name, second_name), person_type, choice_live)
        status_messages['status'] = 'ok'
        new_person.office = None
        msg = "{} {} {} has been successfully added.".format(person_type, first_name, second_name)
        status_messages['message'].append(msg)
    except TypeError:
        msg = ""
        status_messages['message'].append(msg)
        return status_messages

    if isinstance(new_person, model.Staff):
        #add to dojo
        dojo.add_staff(new_person)
        index_office = choose_office_random(dojo)
        if index_office != "NoRoomException" and \
        not dojo.get_office_at_index(index_office).is_full():

            dojo.add_person_office(index_office, new_person)
            office = dojo.get_office_at_index(index_office)
            new_person.office = True
            msg = "{} has been allocated the office {}".format(new_person.name, office.name)
            status_messages['message'].append(msg)
        else:
            #change status to not added no room
            msg = "{} not has been allocated the office".format(new_person.name)
            status_messages['message'].append(msg)
    elif isinstance(new_person, model.Fellow):
        #add to dojo
        dojo.add_fellow(new_person)

        #generate random indexes
        index_livingspace = choose_living_space_random(dojo)
        index_office = choose_office_random(dojo)

        #assign fellow office
        if index_office != "NoRoomException" and \
        not dojo.get_office_at_index(index_office).is_full():

            dojo.add_person_office(index_office, new_person)
            office = dojo.get_office_at_index(index_office)
            new_person.office = True
            msg = "{} has been allocated the office {}".format(new_person.name, office.name)
            status_messages['message'].append(msg)
        else:
            msg = "{} has not been allocated an office".format(new_person.name)
            status_messages['message'].append(msg)

        #assign fellow living space
        if index_livingspace == "NoRoomException" or \
        dojo.get_livingspace_at_index(index_livingspace).is_full():

            msg = "{} not has been allocated a livingspace".format(new_person.name)
            status_messages['message'].append(msg)
        elif new_person.wants_living:
            dojo.add_fellow_living(index_livingspace, new_person)
            livingspace = dojo.get_livingspace_at_index(index_livingspace)
            new_person.livingspace = True
            msg = "{} has been allocated the livingspace {} ".format(new_person.name, livingspace.name)
            status_messages['message'].append(msg)
    elif new_person == 'Invalid name':
        status_messages['status'] = 'Invalid name'
        msg =  "{} {} has not been  added  ".format(person_type, name)
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
    rooms = dojo.office + dojo.livingspace
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
    rooms = dojo.office + dojo.livingspace
    for room in rooms:
        allocations[room.name] = people_inroom(dojo, room.name)

    return allocations

def list_unallocated(dojo, file_name = ''):
    """
    returns a list of unallocated people to the screen
    if file_name is specified values are saved txt
    """
    unallocated = []
    person = dojo.person

    #go over fellow first
    for fellow in person['fellow']:
        if (not fellow.is_allocated_living()) or (not fellow.is_allocated_office()):
            unallocated.append(fellow)
    #go over staff
    for staff in person['staff']:
        if not staff.is_allocated_office():
            unallocated.append(staff)
    return unallocated

def save_data_txt(file_name, raw_data, mode = 'wt'):
    data = []
    for person in raw_data:
        if isinstance(person, model.Fellow):
            wants_living = 'N'
            if person.wants_living:
                wants_living = 'Y'
            user_info = person.name.upper() + "  FELLOW  " + wants_living
        else:
            user_info = person.name.upper() + "  STAFF  "
        if user_info not in data:
            data.append(user_info)
    file_out = open(file_name + '.txt', mode)
    for name in data:
        print(name, file=file_out)
    file_out.close()

def reallocate_person(room_name, person_id, dojo):
    find_person = None
    find_person_type = ''
    find_room = None
    find_room_type = ''
    find_current_room = None
    person_id = int(person_id)
    #get the person and their type brute force
    for type_person in dojo.person:
        for person in dojo.person[type_person]:
            print(person.id)
            if person.id == person_id:
                find_person = person
                find_person_type = type_person
                break
    if not find_person:
        return "Person not found"

    #get the room brute force
    room_name = room_name.strip().lower()
    if not room_name in dojo.takken_names :
        return "Room not found"
    else:
        for room_type in dojo.rooms:
            for room in dojo.rooms[room_type]:
                if room.name == room_name:
                    find_room = room
                    find_room_type = room_type
                if find_person in room.occupants:
                    find_current_room = room

    #handle reallocating fellow to livingspaces
    if find_person_type == 'fellow':
        if find_room_type == 'livingspace':
            #check to see if fellow what's living space
            if not find_person.wants_living:
                return "Invalid Operation"
            #remove them in previoius room
            if find_person.is_allocated_living:
                find_current_room.remove(find_person)
            #allocate living space
            index = choose_living_space_random(dojo)
            new_room = dojo.rooms['livingspace'][index]
            new_room.add_occupant(find_person)
            find_person.livingspace = True

    #staff not allowed to have living space
    if find_person_type == 'staff':
        if find_room_type == 'livingspace':
            return "Invalid operations"

    #handle office reallocation
    if find_room_type == 'offices':
        print("Changing........")
        if find_current_room:
            find_current_room.remove(find_person)
        index= choose_office_random(dojo)
        new_room = dojo.rooms['offices'][index]
        new_room.add_occupant(find_person)
        find_person.office = True
    return 'Done'
