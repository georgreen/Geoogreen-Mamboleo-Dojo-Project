import csv
import random

from models import model

def choose_office_random(dojo):
    """
    choose an office at random
    """
    number_of_offices = len(dojo.office)
    if number_of_offices > 0:
        index = random.randrange(number_of_offices)
    else:
        return "NoRoomException"
    return index

def choose_living_space_random(dojo):
    """
    choose a livingspace at random
    """
    number_of_livingspace = len(dojo.livingspace)
    if number_of_livingspace > 0:
        index = random.randrange(number_of_livingspace)
    else:
        return "NoRoomException"
    return index

class NoRoomException(Exception):
    pass

def save_data_txt(file_name, raw_data, mode = 'wt'):
    data = []
    for person in raw_data:
        if isinstance(person, model.Fellow):
            wants_living = 'N'
            if person.wants_living:
                wants_living = 'Y'
            user_info = person.name.upper() + "  FELLOW  " + wants_living
        else:
            user_info = person.name.upper() + "  STAFF  "
        if user_info not in data:
            data.append(user_info)
    file_out = open(file_name + '.txt', mode)
    for name in data:
        print(name, file=file_out)
    file_out.close()

def load_data_txt(file_name):
    data = []
    raw_data = open(file_name, 'rt')
    while True:
        store = []
        line = raw_data.readline()
        if not line:
            break
        data.append(line.split())
    return data
