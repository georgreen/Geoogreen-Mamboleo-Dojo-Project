# -*- coding: utf-8 -*-
import os
from docopt import docopt, DocoptExit
import cmd
from models import model
from views import ui, template
from core import logic


class Admin(cmd.Cmd):
    # my shell promt format
    prompt = "INPUT $ > "

    def __init__(self, name):
        cmd.Cmd.__init__(self)
        self.name = name
        self.dojo = model.Dojo(self.name)

    def argument_parser(fn):
        '''
        input fn -> function
        return -> a fuction that can parse commandline args using docopt.
        '''
        def get_args(self, args):
            try:
                opt = docopt(fn.__doc__, args)
                return fn(self, opt)
            except DocoptExit as e:
                ui.print_error(e)

        return get_args

    @argument_parser
    def do_create_room(self, room_information):
        """
        Usage:
           create_room <room_type> <room_name>...
        """
        room_type = room_information['<room_type>']
        for name in room_information['<room_name>']:
            status_message = logic.create_and_addroom(self.dojo, room_type, name)
            ui.createroom_ui(status_message)

    @argument_parser
    def do_add_person(self, person_information):
        """
        Usage:
            add_person <firstname> <secondname> <person_type> [<choice>]
        """
        firstname = person_information['<firstname>']
        secondname = person_information['<secondname>']
        wants_room = person_information['<choice>']
        person_type = person_information['<person_type>']

        status_messages = logic.addsperson_chooseroom(self.dojo, firstname, secondname, person_type, wants_room)
        ui.person_ui(status_messages)

    @argument_parser
    def do_print_room(self, room_name):
        """
        Usage:
            print_room <room_name>
        """
        room_name = room_name['<room_name>']
        try:
            occupants = logic.people_inroom(self.dojo, room_name)
            ui.room_ui(room_name, occupants)
        except logic.NotFoundException:
            ui.room_ui(room_name, found=False)

    @argument_parser
    def do_print_allocations(self, file_name):
        """
        Usage:
            print_allocations [<-o=FILE>]
        """
        allocations = logic.dict_allocations(self.dojo)
        file_name = file_name['<-o=FILE>']
        if file_name:
            mode = 'wt'
            for raw_data in allocations.values():
                logic.save_data_txt(file_name, raw_data, mode)
                mode = 'at'
            ui.print_message("Data saved succefully to file: " + file_name)
        else:
            ui.allocations_ui(allocations)

    @argument_parser
    def do_print_unallocated(self, file_name):
        """
        Usage:
            print_unallocations [<-o=FILE>]
        """
        file_name = file_name['<-o=FILE>']
        unallocated_person = logic.list_unallocated(self.dojo)
        if file_name:
            logic.save_data_txt(file_name, unallocated_person)
            ui.print_success("Data saved succefully to file: " + file_name)
        else:
            ui.unallocated_ui(unallocated_person)

    @argument_parser
    def do_reallocate_person(self, reallocate_information):
        """
        Usage:
            reallocate_person <person_id> <new_room_name>
        """
        room_name = reallocate_information['<new_room_name>']
        person_id = reallocate_information['<person_id>']
        status = logic.reallocate_person(room_name, person_id, self.dojo)
        ui.print_message(status)

    @argument_parser
    def do_load_people(self, file_name):
        """
        Usage:
            load_people <file_name>
        """
        file_name = file_name['<file_name>']
        status_messages = logic.load_data_txt(file_name, self.dojo)

        for status in status_messages:
            if status['status'] == 'filenotfound':
                ui.print_error(status['message'])
            elif status['status'] == 'illegalformat':
                ui.print_warning(status['message'], status='Invalid format')
            else:
                ui.person_ui(status)

    def do_top(self, args):
        '''
        Usage:
        top
        '''
        ui.clear_console()

    def do_quit(self, args):
        '''
        Usage:
        quit
        '''
        ui.print_exit()
        exit(0)

    def do_restart(self, args):
        '''
        Usage:
        restart
        '''
        ui.clear_console()
        os.system('python3 admin.py')


if __name__ == '__main__':
    App = Admin("Andela-Kenya")
    try:
        ui.print_welcome()
        ui.print_usage()
        App.cmdloop()
    except KeyboardInterrupt:
        ui.print_exit()
        exit(0)
