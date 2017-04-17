# -*- coding: utf-8 -*-
import os
from docopt import docopt, DocoptExit
import cmd
from models import model
from views import ui, template
from core import logic


class Dojo(cmd.Cmd):
    def __init__(self, name):
        cmd.Cmd.__init__(self)
        self.name = name
        self.dojo = model.Dojo(self.name)

    # my shell promt format
    prompt = "INPUT $ > "
    ui.print_welcome()
    ui.print_usage()

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

    def do_create_room(self, args):
        """
        Usage:
           create_room <room_type> <room_name>...
        """
        try:
            room_information = docopt(self.do_create_room.__doc__, args)
        except DocoptExit as e:
            ui.print_message(e)
        else:
            room_type = room_information['<room_type>']
            for name in room_information['<room_name>']:
                status_message = logic.create_and_addroom(self.dojo, room_type, name)

                # call ui from views to display our status messages
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
                ui.print_template_room(message, room_type, room_name, fail=fail, status=status)

    def do_add_person(self, args):
        """
        Usage:
            add_person <firstname> <secondname> <person_type> [<choice>]
        """
        try:
            person_information = docopt(self.do_add_person.__doc__, args)
        except DocoptExit as e:
            ui.print_message(e)
        else:
            firstname = person_information['<firstname>']
            secondname = person_information['<secondname>']
            wants_room = person_information['<choice>']
            person_type = person_information['<person_type>']

            status_messages = logic.addsperson_chooseroom(self.dojo,firstname, secondname, person_type, wants_room)
            self.person_ui(status_messages)

    def person_ui(self, status_messages):
        status = status_messages['status']
        name = status_messages['name']
        person_type = status_messages['person_type']

        if status == 'Failed':
            message = template.person_not_created_message
            ui.print_template_room(message, person_type, name, person_type, fail=True, status='Failed')
        elif status == 'ok':
            choice = status_messages['choice_live']
            office = status_messages['office']
            livingspace = status_messages['livingspace']

            # dispaly person created flush
            message = template.person_created_message
            ui.print_template_room(message, person_type, name)

            if office:
                message = template.allocated_office_message
                ui.print_template_room(message, name, office)
            else:
                message = template.not_allocated_office_message
                ui.print_template_room(message, name, fail=True, status='No Room Available')

            if person_type == 'fellow':
                if livingspace and choice:
                    message = template.allocated_living_message
                    ui.print_template_room(message, name, livingspace)
                elif choice and not livingspace:
                    message = template.not_allocated_living_message
                    ui.print_template_room(message, name, fail=True, status='No Room Available')

    def do_print_room(self, args):
        """
        Usage:
            print_room <room_name>
        """
        try:
            room_name = docopt(self.do_print_room.__doc__, args)
        except DocoptExit as e:
            ui.print_message(e)
        else:
            ui.print_message("Room :" + room_name['<room_name>'])
            ui.print_message("_" * len("Room :" + room_name['<room_name>']))
            try:
                occupants = logic.people_inroom(self.dojo, room_name['<room_name>'])
                if len(occupants) > 0:
                    ui.print_room_members(occupants)
                else:
                    ui.print_message("Empty room :-( ")
            except logic.NotFoundException:
                ui.print_message("Room Not Found :-( ")
            ui.print_message(" ")

    def do_print_allocations(self, args):
        """
        Usage:
            print_allocations [<-o=FILE>]
        """
        try:
            file_name = docopt(self.do_print_allocations.__doc__, args)
        except DocoptExit as e:
            ui.print_message(e)
        else:
            allocations = logic.dict_allocations(self.dojo)
            if file_name['<-o=FILE>']:
                mode = 'wt'
                for raw_data in allocations.values():
                    logic.save_data_txt(file_name['<-o=FILE>'], raw_data, mode)
                    mode = 'at'
                ui.print_message("Data saved succefully to file: " + file_name['<-o=FILE>'])
            else:
                empty = True
                for room_name in allocations:
                    empty = False
                    ui.print_message("Room :" + room_name)
                    ui.print_message("_" * len("Room :" + room_name))

                    if len(allocations[room_name]) > 0:
                        ui.print_room_members(allocations[room_name])
                        print(" ")
                    else:
                        ui.print_message("Empty room :-( ")
                if empty:
                    ui.print_message("No Allocations are available")

    def do_print_unallocated(self, args):
        """
        Usage:
            print_unallocations [<-o=FILE>]
        """
        try:
            file_name = docopt(self.do_print_unallocated.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
        else:
            unallocated_person = logic.list_unallocated(self.dojo)
            if file_name['<-o=FILE>']:
                logic.save_data_txt(file_name['<-o=FILE>'], unallocated_person)
                ui.print_message("Data saved succefully to file: " + file_name['<-o=FILE>'])
            else:
                ui.print_message("*" * 40)
                ui.print_message('      LIST OF UNALLOCATED PEOPLE')
                ui.print_message("*" * 40)

                # build display message
                if len(unallocated_person) > 0:
                    user_info = ''
                    for person in unallocated_person:
                        user_info = person.name.upper()
                        if isinstance(person, model.Fellow):
                            wants_living = 'N'
                            user_info += "  FELLOW "
                            if person.wants_living:
                                wants_living = 'Y'
                            user_info += wants_living
                        else:
                            user_info += "  STAFFF   "
                        ui.print_not_allocated(user_info)
                else:
                    ui.print_message("Every one is allocated ;-)")

    def do_reallocate_person(self, args):
        """
        Usage:
            reallocate_person <person_id> <new_room_name>
        """
        try:
            reallocate_information = docopt(self.do_reallocate_person.__doc__, args)
        except DocoptExit as e:
            ui.print_message(e)
        else:
            room_name = reallocate_information['<new_room_name>']
            person_id = reallocate_information['<person_id>']
            status = logic.reallocate_person(room_name, person_id, self.dojo)
            ui.print_message(status)

    def do_load_people(self, args):
        """
        Usage:
            load_people <file_name>
        """
        try:
            file_name = docopt(self.do_load_people.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
        else:
            file_name = file_name['<file_name>']
            status_messages = logic.load_data_txt(file_name, self.dojo)

            for status in status_messages:
                if status['status'] == 'filenotfound':
                    ui.print_message(status['message'])
                elif status['status'] == 'illegalformat':
                    ui.print_message(status['message'])
                else:
                    self.person_ui(status)


if __name__ == '__main__':
    App = Dojo("Andela-Kenya")
    try:
        App.cmdloop()
    except KeyboardInterrupt:
        ui.print_exit()
        exit(0)
