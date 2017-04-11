from context import *
from core import logic
from docopt import docopt, DocoptExit
import cmd

class App(cmd.Cmd):
    #my shell promt format
    prompt = "INPUT $ > "

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
                    pass
                except TypeError:
                    #get view for this
                    pass
                if new_room == 'Invalid name':
                    #get view for this
                    pass
                else:
                    #call add room to dojo
                    pass
        #call ui from views to display our status messages

if __name__ == '__main__':
    App().cmdloop()
