from models.base_db import Base, Boolean, Column, ForeignKey, Integer, String


class Person(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    office = Column(Boolean, default=False)
    type = Column(String(50))
    room_id = Column(Integer, ForeignKey('rooms.id'))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'users'
    }

    # number of Person
    number_of_person = 0

    def __init__(self, name):
        Person.number_of_person += 1
        self.id = Person.number_of_person
        self.name = name
        self.office = False

    def remove_office(self):
        self.office = None

    def is_allocated_office(self):
        return self.office


class Fellow(Person):
    # number of fellows
    number_of_fellows = Column(Integer, default=0)
    wants_living = Column(Boolean, default=False)
    livingspace = Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_identity': 'fellow'
    }

    def __init__(self, name, wants_living=False):
        Fellow.number_of_fellows += 1
        Person.__init__(self, name)
        self.wants_living = wants_living
        self.livingspace = False

    def is_allocated_living(self):
        return self.livingspace

    def remove_livingspace(self):
        self.livingspace = False

    def __str__(self):
        choice = 'Y' if self.wants_living else 'N'
        name = self.name.upper()
        return "FELLOW %s %s ID %d" % (name, choice, self.id)


class Staff(Person):
    # number of Staff
    number_of_staff = Column(Integer, default=0)

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

    def __init__(self, name):
        Staff.number_of_staff += 1
        Person.__init__(self, name)

    def __str__(self):
        name = name = self.name.upper()
        return "STAFF %s ID %d" % (name, self.id)
