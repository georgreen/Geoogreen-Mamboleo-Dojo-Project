# -*- coding: utf-8 -*-
from pyfiglet import figlet_format
from termcolor import cprint, colored
from views import template

import os

unicode_tick = u'\u2713'
unicode_cross = u'\u274c'
unicode_warning = u'\u26A0'
unicode_stop = u'\u26d4'

# emojies
unicode_winkface = u"\U0001F609"
unicode_coolface = u"\U0001F60E"
unicode_sadface = u"\u2639"
unicode_luckyface = u"\U0001F61B"


def print_welcome():
    '''
    display welcome message
    '''
    clear_console()
    msg = "Office LivingSpace Allocation System "
    cprint(figlet_format(msg), 'blue', attrs=['bold'])
    print_message("Welcome to Office Space Allocation")


def print_exit():
    '''
    display exit message
    '''
    clear_console()
    print_message("Exiting system now....")
    cprint(figlet_format("GoodBye!"), 'blue', attrs=['bold'])


def print_usage():
    '''
    print usage message on clear_console
    '''
    usage = """
    Usage:
        create_room <room_type> <room_name> ...
        add_person <first_name> <last_name> <FELLOW>|<STAFF> [<wants_accommodation>]
        print_room <room_name>
        print_allocations <filename>
        print_unallocated <filename>
        reallocate_person <person_identifier> <new_room_name>
        load_people <filename>
        clear
        restart
        quit

    Arguments:
        FELLOW|STAFF           Person type to create
        wants_accommodation    Specify if fellow wants a living space
        filename               Specify file to load or read data from

    Options:
        -h, --help           : To show the command's help messsage
    """
    print(usage)


def clear_console():
    '''
    clear's the clear_console
    '''
    os.system('clear')


def print_message(msg, status="", symbole="", color='green'):
    padding = 80
    msg_len = 10
    if type(msg) == str:
        msg_len = padding - len(msg)
    print(' ' * 5, colored(msg, color), " " * msg_len, end=' ')
    print(colored(status, color), colored(symbole, color))


def print_error(msg, status='Error', c='red'):
    print_message(msg, status=status, symbole=unicode_stop, color=c)


def print_warning(msg, status="Warning", c='yellow'):
    print_message(msg, status=status, symbole=unicode_warning, color=c)


def print_success(msg, status="Success", c='green'):
    print_message(msg, status=status, symbole=unicode_tick, color=c)


def print_not_allocated(user_info, color='white'):
        print_message(user_info, color=color)


def print_template(template, *data, fail=False, status='ok', Id=None):
    '''
    prints templates with the given color and status message
    '''
    padding = 70
    symbole = unicode_tick
    color = 'green'
    if fail:
        symbole = unicode_cross
        color = 'red'
        if status == 'Duplicate name' or status == 'No Room Available':
            symbole = unicode_warning
            color = 'blue'

    col_str = template % data
    id_padd = padding - len(col_str)
    st_padd = 10
    print(' ' * 5, colored(col_str, color), " " * id_padd, end='')
    if Id:
        col_id = 'ID:' + str(Id)
        st_padd = st_padd - len(col_id)
        print(colored(col_id, 'green'), end='')
    print(" " * st_padd, colored(status, color), colored(symbole, color))


def createroom_ui(status_message):
    room_type = status_message['room_type']
    room_name = status_message['room_name']
    status = status_message['status']
    messsage = None
    color = None
    fail = True
    if status_message['status'] == 'ok':
        message = template.room_created_message
        fail = False
    elif status_message['status'] == 'failed':
        message = template.room_typeerror_message
    elif status_message['status'] == 'Duplicate name':
        message = template.room_dup_name_message
    elif status_message['status'] == 'Invalid name':
        message = template.room_not_created_message
    print_template(message, room_type, room_name, fail=fail, status=status)


def person_ui(status_messages):
    status = status_messages['status']
    name = status_messages['name'].lower().capitalize()
    person_type = status_messages['person_type'].lower().capitalize()
    Id = status_messages['id']

    if status == 'Failed':
        message = template.person_not_created_message
        p_t = person_type
        print_template(message, p_t, name, p_t, fail=True, status='Failed')
    elif status == 'ok':
        choice = status_messages['choice_live']
        office = status_messages['office']
        livingspace = status_messages['livingspace']

        # dispaly person created flush
        message = template.person_created_message
        print_template(message, person_type, name, Id=Id)
        if office:
            message = template.allocated_office_message
            print_template(message, name, office)
        else:
            message = template.not_allocated_office_message
            status = 'No Room Available'
            print_template(message, name, fail=True, status=status)

        if person_type == 'Fellow' and choice:
            if not livingspace:
                message = template.not_allocated_living_message
                status = 'No Room Available'
                print_template(message, name, fail=True, status=status)
            else:
                message = template.allocated_living_message
                print_template(message, name, livingspace)


def unallocated_ui(unallocated_person):
    print_message("*" * 40)
    print_message('      LIST OF UNALLOCATED PEOPLE')
    print_message("*" * 40)
    # build display message
    if len(unallocated_person) > 0:
        for user_info in unallocated_person:
            print_not_allocated(user_info, color='blue')
    else:
        print_message("Every one is allocated ", symbole=unicode_winkface)


def room_ui(room_name, occupants=None, found=True):
    color = 'green'
    if not found:
        color = 'red'
    print_message("Room :" + room_name, color=color)
    print_message("_" * 20, color=color)
    if found:
        if len(occupants) > 0:
            print(' ' * 5, end='')
            for member in occupants:
                name = colored(member.name.capitalize(), 'green')
                print(name, end=', ')
            print(end='\n')
        else:
            print_message("Empty room", symbole=unicode_sadface, color='blue')
    else:
        print_error("Room not found", status='Not Found')
    print(end='\n \n')


def allocations_ui(allocations):
    empty = True
    for room_name in allocations:
        empty = False
        room_ui(room_name, allocations[room_name])
    if empty:
        print_message("No Allocations are available", color='yellow')


def reallocate_ui(status_message):

    if status_message['status'] == 'Fail':
        print_error(status_message['message'])
        return
    # prepare data to be displayed
    room_type = 'Office'
    pre_room = status_message['prev_office']
    if status_message['room_type'] == 'L':
        room_type = 'LivingSpace'
        pre_room = status_message['prev_livingspace']
    name = status_message['name'].lower().capitalize()
    if not pre_room:
        pre_room = 'No where !'
    else:
        pre_room = pre_room.name
    curr_room = status_message['current_room']

    if status_message['status'] == 'ok':
        msg = template.reallocate_person_message
        print_template(msg, name, room_type, curr_room, pre_room)
    elif status_message['status'] == 'Invalid Operation':
        msg = template.invalid_reallocation
        status = 'Invalid Reallocation'
        if status_message.get('choice') or room_type == 'Office':
            status = 'Room Full'
        print_template(msg, name, room_type, curr_room, fail=True, status=status)
