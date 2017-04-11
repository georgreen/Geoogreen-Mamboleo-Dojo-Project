from context import *
from core import logic
from docopt import docopt, DocoptExit
from views import ui
import cmd

class App(cmd.Cmd):
    #my shell promt format
    prompt = "INPUT $ > "
    logic.dojo = logic.init_app()

    def do_create_room(self, args):
        """
        Usage:
           create_room <room_type> <room_name>...
        """
        #alist of all status message form create room
        status_messages = []

        try:
            room_information = docopt(self.do_create_room.__doc__, args)
            print(room_information)
        except DocoptExit as e:
            print(e)
            #call view to display Error message
        except KeyboardInterrupt:
            pass
        else:
            for name in room_information['<room_name>']:
                try:
                    #call helper to create this
                    status_messages.append(logic.helper_create_and_addroom(room_information['<room_type>'], name))
                except TypeError:
                    #get view for this
                    status_messages.append("Please type in a proper type")
                    break


        #call ui from views to display our status messages

if __name__ == '__main__':
    App().cmdloop()
