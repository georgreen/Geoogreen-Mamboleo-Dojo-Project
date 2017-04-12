from context import models
from models import model
import random


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

def helper_create_and_addroom(dojo, room_type, room_name):
    status_messages = {'status': None, 'message' : None}
    new_room = create_room(room_type, room_name)

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
    else:
        #give some status messge
        status_messages['status'] = 'Invalid name'


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
