import cmd
import os
import shutil

from core import logic
from docopt import DocoptExit, docopt
from models import model
from views import template, ui


class Admin(cmd.Cmd):
    # my shell promt format
    prompt = ui.dynamic_promt()

    def __init__(self, name, db=False):
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
                Admin.prompt = ui.dynamic_promt()
                return fn(self, opt)
            except DocoptExit as e:
                ui.print_error(e, status="Malformed Command")
                Admin.prompt = ui.dynamic_promt(color='red',
                                                symbole=ui.unicode_sadface)
        return get_args

    @argument_parser
    def do_create_room(self, room_information):
        """
        Args:
            room_information (str): captures room informatin i.e name and type
                                    they should be separate by a space.

        Returns:
            None: The return value.

        Example:
              >>> create_room office red
              >>> create_room livingspace blue green yellow black

        Usage:
            create_room <room_type> <room_name>...
        """
        room_t = room_information['<room_type>']
        for name in room_information['<room_name>']:
            status_message = logic.create_and_addroom(self.dojo, room_t, name)
            ui.createroom_ui(status_message)

    @argument_parser
    def do_add_person(self, person_information):
        """
        Args:
            person_information (str): captures person informatin i.e name,
                          type and choice they should be separate by a space.


        Returns:
            None: The return value.

        Example:
              >>> add_person Georgreen Ngunga Fellow Y
              >>> add_person John Doe Staff

        Usage:
            add_person <firstname> <secondname> <person_type> [<choice>]
        """

        firstname = person_information['<firstname>']
        secondname = person_information['<secondname>']
        wants_room = person_information['<choice>']
        person_type = person_information['<person_type>']
        if wants_room and wants_room.lower() in "n no":
            wants_room = None
        elif wants_room and wants_room.lower() in "y yes":
            wants_room = 'Y'

        status_messages = logic.addsperson_chooseroom(self.dojo,
                                                      firstname, secondname,
                                                      person_type, wants_room)
        ui.person_ui(status_messages)

    @argument_parser
    def do_print_room(self, room_name):
        """
        Args:
            room_name (str): captures room informatin i.e name

        Returns:
            None: The return value.

        Example:
              >>> print_room red

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
        Args:
            file_name (str): captures file name (optional)

        Returns:
            None: The return value.

        Example:
              >>> print_allocations
              >>> print_allocations file.txt

        Usage:
            print_allocations [<-o=FILE>]
        """

        allocations = logic.dict_allocations(self.dojo)
        file_name = file_name['<-o=FILE>']
        if file_name:
            mode = 'wt'
            for raw_data in allocations.values():
                logic.save_txt(file_name, raw_data, mode)
                mode = 'at'
            ui.print_success("Data saved succefully to file: " + file_name)
        else:
            ui.allocations_ui(allocations)

    @argument_parser
    def do_print_unallocated(self, file_name):
        """
        Args:
            file_name (str): captures file name (optional)

        Returns:
            None: The return value.

        Example:
              >>> print_unallocated
              >>> print_unallocated file.txt

        Usage:
            print_unallocations [<-o=FILE>]
        """

        file_name = file_name['<-o=FILE>']
        unallocated_person = logic.list_unallocated(self.dojo)
        if file_name:
            logic.save_txt(file_name, unallocated_person)
            ui.print_success("Data saved succefully to file: " + file_name)
        else:
            ui.unallocated_ui(unallocated_person)

    @argument_parser
    def do_reallocate_person(self, reallocate_information):
        """
        Args:
            reallocate_information(str): captures information for reallocating
                                         the given user i.e user id and room to
                                         be reallocated to.

        Returns:
            None: Returns none

        Example:
            >>> reallocate_person 1 red

        Usage:
            reallocate_person <person_id> <new_room_name>
        """

        room_name = reallocate_information['<new_room_name>']
        person_id = reallocate_information['<person_id>']
        status = logic.reallocate_person(room_name, person_id, self.dojo)
        ui.reallocate_ui(status)

    @argument_parser
    def do_load_people(self, file_name):
        """
        Args:
            file_name (str): captures file name

        Returns:
            None: The return value.

        Example:
              >>> load_people file.txt

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

    @argument_parser
    def do_load_state(self, database_name):
        """
        Args:
            database_name (str): absolute path specifying  a database

        Returns:
            None: The return value.

        Example:
            >>> load_state sqlite.db

        Usage:
             load_state <‐‐db=sqlite_database> [<overwrite_internal_state>]
        """

        message = ""
        success = False
        user_input = None
        if database_name["<overwrite_internal_state>"] not in ["No", "no"]:
            ui.print_warning(template.promt_postload_message)
            user_input = input(" ->: ")
        if not user_input or user_input.lower() != "no":
            try:
                self.dojo.load_state(database_name["<‐‐db=sqlite_database>"])
                message = "Database succesfully Loaded! "
                success = True
            except model.DBDoesNotExistException:
                message = "Database Doese not exist!"
        else:
            message = "Load state aborted !"
        if success:
            ui.print_success(message)
        else:
            ui.print_error(message, status='STOPPED ')
            Admin.prompt = ui.dynamic_promt(color='red',
                                            symbole=ui.unicode_sadface)

    @argument_parser
    def do_save_state(self, database_name):
        """
        Args:
            database_name (str): absolute path specifying a database

        Returns:
            None: The return value.

        Example:
            >>> save_state sqlite.db

        Usage:
             save <sqlite_database>
        """

        success = True
        message = "Failed"

        try:
            self.dojo.save_state(database_name["<sqlite_database>"])
            message = "Success saved database"
        except model.UpdateException:
            ui.print_message(template.promt_updatedb_message)
            user_input = input(" ->: ")
            if user_input.lower() == 'yes':
                self.dojo.save_state(database_name["<sqlite_database>"],
                                     up=False)
                message = "Updating Database"
            elif user_input.lower() == 'no':
                try:
                    self.dojo.save_state(database_name["<sqlite_database>"],
                                         over_write=True)
                except model.OverWriteException:
                    self.dojo.save_state(database_name["<sqlite_database>"])
                    message = "Over Writing Database"
            else:
                message = "Wrong Choise Databese not saved try again"
                success = False
        except Exception:
            message = "Something Went Wrong"
            success = False
        if success:
            ui.print_success(message)
        else:
            ui.print_error(message)
            Admin.prompt = ui.dynamic_promt(color='red',
                                            symbole=ui.unicode_sadface)

    def do_clear(self, args):
        """
        Args:
            None : does not take arguments

        Returns:
            None: The return value.

        Example:
            >>> clear

        Usage:
              clear
        """
        ui.clear_console()

    def do_quit(self, args):
        """
        Args:
            None : does not take arguments

        Returns:
            None: The return value.

        Example:
            >>> quit

        Usage:
              quit
        """

        try:
            if os.path.exists("models/database/default.db"):
                self.dojo.save_state(up=False)
            else:
                if self.dojo.database_name:
                    source = "models/database/" + self.dojo.database_name
                    destination = "models/database/" + "default.db"
                    shutil.copy(source, destination)
        except Exception:
            ui.print_error("State not saved")
        ui.print_exit()
        return True

    def do_restart(self, args):
        """
        Args:
            None : does not take arguments

        Returns:
            None: The return value.

        Example:
            >>> restart

        Usage:
              restart
        """

        ui.print_warning(template.user_warning_message)
        user_input = input(" ->: ")
        if user_input.lower() != "no":
            raise SystemRestartInterrupt
        else:
            ui.print_warning("Restart Aborted !")
            Admin.prompt = ui.dynamic_promt(color='red',
                                            symbole=ui.unicode_sadface)

    def do_EOF(self):
        return True

    def emptyline(self):
        ui.print_error("Please Type A Command.", status='EMPTY LINE')
        ui.print_message(template.help_user_message)
        Admin.prompt = ui.dynamic_promt(color='red',
                                        symbole=ui.unicode_sadface)

    def default(self, args):
        invalid_command = args.split(' ')[0]
        ui.print_error(invalid_command, status='Command Does Not Exit')
        ui.print_message(template.help_user_message)
        Admin.prompt = ui.dynamic_promt(color='red',
                                        symbole=ui.unicode_sadface)

    @argument_parser
    def do_remove_person(self, person_information):
        """
        Args:
            person_information (int): user id

        Returns:
            None: The return value.

        Example:
            >>> remove_person 1

        Usage:
            remove_person <ID>
        """

        user_id = person_information["<ID>"]
        validated = None
        try:
            user_id = int(user_id)
            validated = True
        except Exception:
            validated = False
            ui.print_error("Invalid User Id, User Integers e.g 12")
            Admin.prompt = ui.dynamic_promt(color='red',
                                            symbole=ui.unicode_sadface)
        if validated and self.dojo.get_person(user_id):
            user = self.dojo.get_person(user_id)
            if self.dojo.is_staff(user):
                self.dojo.remove_staff(user)
                ui.print_warning(user.__str__(), status="Staff was Removed")
            else:
                self.dojo.remove_fellow(user)
                ui.print_warning(user.__str__(), status="Fellow was Removed")
        elif validated:
            ui.print_error("The User does not exist",
                           status='Id does not Exist')

    @argument_parser
    def do_remove_room(self, room_name):
        """
        Args:
            room_name (str): room's name

        Returns:
            None: The return value.

        Example:
            >>> remove_room red

        Usage:
            remove_room <room_name>
        """

        room_name = room_name["<room_name>"]
        office = self.dojo.get_office(room_name)
        livingspace = self.dojo.get_livingspace(room_name)
        if office:
            self.dojo.remove_office(office)
            ui.print_warning("Office:" + office.name, status="Removed")
        elif livingspace:
            self.dojo.remove_livingspace(livingspace)
            ui.print_warning("Livingspace:" + livingspace.name,
                             status="Removed")
        else:
            ui.print_error("The room does not exist", status='Room Not Found')
            Admin.prompt = ui.dynamic_promt(color='red',
                                            symbole=ui.unicode_sadface)

    @argument_parser
    def do_person_information(self, person_information):
        """
        Args:
            person_information (str): specify's person information

        Returns:
            None: The return value.

        Example:
            >>> person_information
            >>> person_information fellow
            >>> person_information staff
            >>> person_information fellow 23
            >>> person_information staff  34

        Usage:
            person_information [<type>] [<id>]
         """
        status_message = {"status": None, "message": None}
        user_id = person_information["<id>"]
        user_type = person_information["<type>"]

        staff = list(self.dojo.staff)
        fellow = list(self.dojo.fellow)
        people = staff + fellow
        # validate user input
        validated = None
        if user_id:
            try:
                user_id = int(user_id)
                validated = True
            except Exception:
                validated = False
            status_message["validated"] = validated

        if user_type and user_type.lower() in ["staff", "fellow"]:
            user_type = user_type.lower()
            if user_id and user_type and validated:
                people = self.dojo.get_person(user_id)
                status_message["status"] = "failed"
                if not people:
                    status_message["message"] = "User not found"
                elif self.dojo.is_fellow(people) and user_type != "fellow":
                    status_message["message"] = "User not staff"
                elif self.dojo.is_staff(people) and user_type != "staff":
                    status_message["message"] = "User not fellow"
                else:
                    status_message["status"] = "ok"
                people = [people]
            elif user_type and validated is None:
                status_message["status"] = "ok"
                people = fellow
                if user_type == "staff":
                    people = staff
            else:
                status_message["status"] = "Invalid ID"
        elif user_type:
            Admin.prompt = ui.dynamic_promt(color='red',
                                            symbole=ui.unicode_sadface)
            people = None
            status_message["status"] = "Invalid type"
        else:
            status_message["status"] = "ok"
        status_message["people"] = people

        ui.person_information_ui(status_message)


class SystemRestartInterrupt(Exception):
    pass


if __name__ == '__main__':
    app = Admin("Andela-Kenya")
    try:
        ui.print_welcome()
        ui.print_usage()
        ui.print_message(template.promt_preload_message)
        user_input = input(" ->: ")
        if user_input.lower() == "yes":
            app.do_load_state("default.db no")
        app.cmdloop()
    except KeyboardInterrupt:
        ui.print_exit()
    except SystemRestartInterrupt:
        ui.clear_console()
        os.system('python3 admin.py')
    except Exception:
        ui.print_error("The Program stopped Abruptly. ERROR!")
