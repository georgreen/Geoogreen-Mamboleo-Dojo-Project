from context import *
from core import logic
from docopt import docopt, DocoptExit
from views import ui
import cmd
from models import model

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
            print_option = docopt(self.do_print_room.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            ui.print_message("NOT YET IMPLEMENTED!")


    def do_print_allocations(self, args):
        """
        Usage:
            print_allocations [-o=filename]​
        """
        try:
            print_option = docopt(self.do_print_allocations.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            ui.print_message("NOT YET IMPLEMENTED!")



    def do_print_unallocated(self, args):
        """
        Usage:
            print_unallocated [-o=filename]
        """
        try:
            print_option = docopt(self.do_print_unallocated.__doc__, args)

        except DocoptExit as e:
            ui.print_message(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            ui.print_message("NOT YET IMPLEMENTED!")



if __name__ == '__main__':
    App().cmdloop()
