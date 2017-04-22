class Person():
    # number of Person
    number_of_person = 0

    def __init__(self, name):
        Person.number_of_person += 1
        self.__id = Person.number_of_person
        self.name = name
        self.office = None

    @property
    def id(self):
        '''
        person's Id based off number of ppl created
        '''
        return self.__id

    def remove_office(self):
        self.office = None

    def is_allocated_office(self):
        return not (not self.office)


class Fellow(Person):
    # number of fellows
    number_of_fellows = 0

    def __init__(self, name, wants_living=False):
        Fellow.number_of_fellows += 1
        Person.__init__(self, name)
        self.wants_living = wants_living
        self.livingspace = False

    def is_allocated_living(self):
        return self.livingspace

    def set_livingspace(self, space):
        if self.wants_living:
            pass

    def remove_livingspace(self):
        self.livingspace = None

    def __str__(self):
        choice = 'Y' if self.wants_living else 'N'
        name = self.name.upper()
        return "FELLOW %s %s" % (name, choice)


class Staff(Person):
    # number of Staff
    number_of_staff = 0

    def __init__(self, name):
        Staff.number_of_staff += 1
        Person.__init__(self, name)

    def __str__(self):
        name = name = self.name.upper()
        return "STAFF %s" % (name)
