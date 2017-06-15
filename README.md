[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4e2474f0bdd34944825080e43e14cf56)](https://www.codacy.com/app/georgreen/Geoogreen-Mamboleo-Dojo-Project?utm_source=github.com&utm_medium=referral&utm_content=georgreen/Geoogreen-Mamboleo-Dojo-Project&utm_campaign=badger)
[![Build Status](https://travis-ci.org/georgreen/Geoogreen-Mamboleo-Dojo-Project.svg?branch=master)](https://travis-ci.org/georgreen/Geoogreen-Mamboleo-Dojo-Project) [![Coverage Status](https://coveralls.io/repos/github/georgreen/Geoogreen-Mamboleo-Dojo-Project/badge.svg?branch=master)](https://coveralls.io/github/georgreen/Geoogreen-Mamboleo-Dojo-Project?branch=master)  [![Code Issues](https://www.quantifiedcode.com/api/v1/project/d4e4bbeca60e46fca5ced46934c26d4c/badge.svg)](https://www.quantifiedcode.com/app/project/d4e4bbeca60e46fca5ced46934c26d4c)


# Office And LivingSpace Allocation System
A Command line application that managers a dojo facillity. <br/>
It allocates rooms to new employees, [Staff or Fellow] randomly.
A room in the dojo can either be an `office` or a `livingspace`. Offices in the dojo can only accommodate 6 people whereas a livingspaces can only accommodate 4.

An employee can either be a `staff` or a `fellow`. Staff can only be assigned offices, whereas fellows can be assigned either or both, depending on there choice regarding a livingspace.

### Available Commands

*	```Adds_room name_room [office | living space]``` <br/>
*	```Adds_Person  firstname secondname [fellow| staff]``` <br/>
*	```Print_Allocations [filename] ``` <br/>
*	```print_Unallocated [filename]``` <br/>
*   ```reallocate_person  id  new_room```<br/>
*   ```load_people  file.txt``` <br/>
*   ```save_state   database_name ```<br/>
*   ```load_state   database_name```<br/>
*   ```remove_person id ```<br/>
*   ```remove_room room_name ```<br/>
*   ```person_information [<type>] [<id>]```<br/>   


## Getting Started

* Create a virtual enviroment <br/>
* Find the instructions for installing and using a virtual environment and virtualenv wrapper [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
* Git Clone this repo to your local machine.
```
git clone https://github.com/georgreenmanu/Geoogreen-Mamboleo-Dojo-Project.git
```


### Prerequisites

```
See requirements.txt
```
You have to install python3 to run this app

### Installing
After cloning the repo , cd to the folder, activate your virtual enviroment then:

```
pip install -r requirements.txt
```
Run the above command to install the app and required dependencies.

### Running the App

From your terminal you can now run the application by using the following command:

```
python3 app.py
```

A welcome screen will show as follows:

   ![home screen](assets/splashscreen.png)

You can now interact with application by entering the commands displayed above. <br/>
*NOTE:* Pressing the TAB key twice displays all the available commands

### Session Examples:
+ To create a room which is an office run the command `create room office red` or use `livingspace` to create a livingspace. You could also give a list of room names to create by separating the names with spaces as shown:

    ![create room](assets/create_room.png)

+ To add a person, use the command `add person Paul Joe staff` and for a fellow who wants a living space use `add person Jojn Doe fellow y`.

    ![add person](assets/add_person.png)

    *NOTE:* the livingspace option only applies to fellows and not staff.

+ You can reallocate a person using the command `reallocate_person <id> <newroom>`.
    ![reallocate](assets/reallocate_person.png)

+ You can load people from a file by using the `load_people file.txt` command.
    ![load_people](assets/load_people.png)


+ You can also print out the allocated people and the unallocated using `print_[allocated|unallocated]` command, specifying the filename saves the allocations on the specified file.
    ![print_unallocated](assets/print_unallocated.png)

    ![print_allocations](assets/print_allocations.png)

+ The command `print_room <room name>` print's room's occupants.
    ![print_room](assets/print_room.png)

+ You can remove_person i.e fellow or staff `remove_person <ID>` remove user from system
    ![remove_person](assets/remove_person.png)

+ You can display everyone or a specific user `person_information [<type>] [<id>]`
    ![person_information](assets/person_information.png)

+ You can delete rooms from the system `remove_room <room_name>`
    ![remove_room](assets/remove_room.png)

+ You could clear the screen if you wish by using the `clear` command.

+ To restart the app use the command `restart`

+ To quit the application run the `quit` command.


## Running the tests

```
nosetests

nosetests --with-coverage  
```
To run tests run the command above : Require's nosetests


## Built With

* [Docopt](http://docopt.org/) - command line argument parser
* [cmd](https://wiki.python.org/moin/CmdModule) - Tool for making command line tools.


## Version
version 4.0


## Authors

* **Georgreen Ngunga**


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* [Stack Overflow](https://stackoverflow.com/)
* [The Hitchhiker’s Guide to Python!](http://python-guide-pt-br.readthedocs.io/en/latest/)

## Future
* Fork me!
