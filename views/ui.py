# -*- coding: utf-8 -*-
from pyfiglet import figlet_format
from termcolor import cprint, colored
import os

unicode_tick = u'\u2713'
unicode_cross = u'\u274c'
unicode_warning = u'\u26A0'


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


def print_message(msg):
    '''
    print message on consle
    '''
    print(msg)


def print_room_members(occupants):
    for member in occupants:
        print(member.name, end=', ')
    print()


def print_not_allocated(user_info):
        print(user_info)


def print_template_room(template, *data, fail=False, status='ok'):
    '''
    prints templates from rooms
    '''
    padding = 8
    symbole = unicode_tick
    color = 'green'
    if fail:
        symbole = unicode_cross
        color = 'red'
        if status == 'Duplicate name':
            symbole = unicode_warning
            color = 'blue'

    print(colored(template % data, color), end='')
    print(" " * padding, colored(status, color), colored(symbole, color))
