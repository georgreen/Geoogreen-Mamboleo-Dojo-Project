def print_welcome():
    '''
    display welcome message
    '''
    print_message("Welcome to Office Space Allocation")

def print_message(msg):
    '''
    print message on consle
    '''
    print(msg)

def print_room_members(occupants):
    for member in occupants:
        print(member.name, end = ', ')
