from context import models, views, core
from core import logic
from views import ui
from docopt import docopt, DocoptExit
import cmd
from models import model
import csv

class App(cmd.Cmd):
    #my shell promt format
    prompt = "INPUT $ > "
    dojo = model.Dojo("Andela-Kenya")
    ui.print_welcome()

    def docopt_helper(function_name):
        pass

    def do_create_room(self,args):
        """
        Usage:
           create_room <room_type> <room_name>...
        """
        #alist of all status message form create room
        status_messages = []

        try:
            room_information = docopt(self.do_create_room.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            for name in room_information['<room_name>']:
                try:
                    #call helper to create this
                    status_messages.append(logic.helper_create_and_addroom(App.dojo,room_information['<room_type>'], name))
                except TypeError:
                    #get view for this
                    status_messages.append({'status' : 'fail', 'message' : "Room type: [{}] can not be  created!".format(room_information['<room_type>'])})


        #call ui from views to display our status messages
        for msg in status_messages:
            ui.print_message(msg['message'])


    def do_add_person(self, args):
        """
        Usage:
            add_person <firstname> <secondname> <person_type> [<choice>]
        """
        status_messages = []
        try:
            person_information = docopt(self.do_add_person.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
        except KeyboardInterrupt:
            pass
        else:
            firstname = person_information['<firstname>']
            secondname = person_information['<secondname>']
            wants_room = person_information['<choice>']
            person_type = person_information['<person_type>']

            status_messages.append(logic.helper_addsperson_chooseroom(App.dojo,firstname, secondname, person_type, wants_room))

        for messages in status_messages:
            for message in messages['message']:
                ui.print_message(message)

    def do_print_room(self, args):
        """
        Usage:
            prtint_room <room_name>
        """
        try:
            room_name = docopt(self.do_print_room.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
        except KeyboardInterrupt:
            pass
        else:
            ui.print_message("Room :" + room_name['<room_name>'])
            ui.print_message("_" * len("Room :" + room_name['<room_name>']))
            try:
                occupants = logic.people_inroom(App.dojo, room_name['<room_name>'])
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
        except KeyboardInterrupt:
            pass
        else:
            allocations = logic.dict_allocations(App.dojo)
            if file_name['<-o=FILE>']:
                mode = 'wt'
                for raw_data in allocations.values():
                    logic.save_data_txt(file_name['<-o=FILE>'], raw_data, mode)
                    mode = 'at'
                ui.print_message("Data saved succefully to file: " + file_name['<-o=FILE>'])
            else:
                for room_name in allocations:
                    ui.print_message("Room :" + room_name)
                    ui.print_message("_" * len("Room :" + room_name))

                    if len(allocations[room_name]) > 0:
                        ui.print_room_members(allocations[room_name])
                    else:
                        ui.print_message("Empty room :-( ")

    def do_print_unallocated(self, args):
        """
        Usage:
            print_unallocations [<-o=FILE>]
        """
        try:
            file_name = docopt(self.do_print_unallocated.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            unallocated_person = logic.list_unallocated(App.dojo)
            if file_name['<-o=FILE>']:
                logic.save_data_txt(file_name['<-o=FILE>'], unallocated_person)
                ui.print_message("Data saved succefully to file: " + file_name['<-o=FILE>'])
            else:
                ui.print_message("*" * 40)
                ui.print_message('      LIST OF UNALLOCATED PEOPLE')
                ui.print_message("*" * 40)

                #build display message
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
            reallocate_person <person_identifier> <new_room_name>
        """
        try:
            reallocate_information = docopt(self.do_reallocate_person.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            room_name = reallocate_information['<new_room_name>']
            person_id = reallocate_information['<person_identifier>']
            status = logic.reallocate_person(room_name, person_id , App.dojo)
            print(reallocate_information)
            print(status)

    def do_load_people(self, args):
        """
        Usage:
            reallocate_person <person_identifier> <new_room_name>
        """
        try:
            reallocate_information = docopt(self.do_reallocate_person.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass



if __name__ == '__main__':
    App().cmdloop()
