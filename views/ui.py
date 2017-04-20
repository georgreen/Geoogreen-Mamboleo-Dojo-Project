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
    cprint(figlet_format("Office LivingSpace Allocation System "), 'white', attrs=['bold'])
    print_message("Welcome to Office Space Allocation")


def print_exit():
    '''
    display exit message
    '''
    clear_console()
    print_message("Exiting system now....")
    cprint(figlet_format("GoodBye!"), 'white', attrs=['bold'])


def print_usage():
    '''
    print usage message on clear_console
    '''
    usage = """
    Usage:
        create room <room_type> <room_name> ...
        add person <first_name> <last_name> <FELLOW>|<STAFF> [<wants_accommodation>]
        print_room <room_name>
        print_allocations <filename>
        print_unallocated <filename>
        reallocate_person <person_identifier> <new_room_name>
        load_people <filename>

    Arguments:
        FELLOW|STAFF           Person type to create
        wants_accommodation    Specify if fellow wants a living space
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
    padding = 8
    print(colored(msg, color), end=' ')
    print(" " * padding, colored(status, color), colored(symbole, color))


def print_error(msg, status='Error'):
    print_message(msg, status=status, symbole=unicode_stop, color='red')


def print_warning(msg, status="Warning"):
    print_message(msg, status=status, symbole=unicode_warning, color='yellow')


def print_success(msg, status="Success"):
    print_message(msg, status=status, symbole=unicode_tick, color='green')


def print_not_allocated(user_info):
        print(user_info)


def print_template(template, *data, fail=False, status='ok'):
    '''
    prints templates with the given color and status message
    '''
    padding = 8
    symbole = unicode_tick
    color = 'green'
    if fail:
        symbole = unicode_cross
        color = 'red'
        if status == 'Duplicate name' or status == 'No Room Available':
            symbole = unicode_warning
            color = 'blue'

    print(colored(template % data, color), end='')
    print(" " * padding, colored(status, color), colored(symbole, color))


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

    if status == 'Failed':
        message = template.person_not_created_message
        print_template(message, person_type, name, person_type, fail=True, status='Failed')
    elif status == 'ok':
        choice = status_messages['choice_live']
        office = status_messages['office']
        livingspace = status_messages['livingspace']

        # dispaly person created flush
        message = template.person_created_message
        print_template(message, person_type, name)

        if office:
            message = template.allocated_office_message
            print_template(message, name, office)
        else:
            message = template.not_allocated_office_message
            print_template(message, name, fail=True, status='No Room Available')

        if person_type == 'Fellow' and choice:
            if not livingspace:
                message = template.not_allocated_living_message
                print_template(message, name, fail=True, status='No Room Available')
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
            print_not_allocated(user_info)
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
            for member in occupants:
                print(colored(member.name.capitalize(), 'green'), end=' ')
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
