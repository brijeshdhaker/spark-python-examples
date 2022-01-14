#
#
#

from uuid import uuid4
from datetime import datetime
from datetime import datetime
import pytz
import random
from faker import Faker
#
class User(object):

    # Class Variable
    CITIES = {
        "IN":["Delhi", "Chennei", "Pune", "Mumbai", "Banglore"],
        "USA": ["New York", "Los Angeles", "Miami"],
        "UK": ["London", "Manchester", "Liverpool", "Oxford"],
        "JP": ["Tokyo", "Osaka", "Yokohama", "Hiroshima"]
    }
    COUNTRIES = ["IN", "USA", "UK", "JP"]
    ROLES = ['Admin', 'Technology']
    NAMES = [
        ("Brijesh K", "brijeshdhaker@gmail.com"),
        ("Neeta K", "neetadhk@gmail.com"),
        ("Keshvi K", "keshvid@gmail.com"),
        ("Tejas K", "tejasd@gmail.com")
    ]

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["id", "uuid", "name", "emailAddr", "age",  "dob", "height", "roles", "status", "addTs", "updTs"]

    # The init method or constructor
    def __init__(self, uuid=None):
        event_datetime = datetime.now(pytz.utc)
        ist_event_datetime = datetime.now(pytz.timezone('Asia/Kolkata'))
        self.addTs = int(event_datetime.strftime("%s"))
        self.updTs = int(event_datetime.strftime("%s"))
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid

    @staticmethod
    def random():

        d1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')

        #print(random_date(d1, d2))
        fake = Faker()
        u = User()
        u.id = random.randint(1000, 5000)
        u.name = fake.name()
        u.emailAddr = fake.email()
        u.age= random.randint(18, 70)
        u.dob= random.randint(18, 70)
        u.height = round(random.uniform(5.0, 7.0))
        u.roles = ['Admin', 'Technology'],
        u.status = 'Active'
        return u

    @staticmethod
    def dict_to_name(obj):
        return User(obj['id'])

    @staticmethod
    def name_to_dict(id):
        return User.to_dict(id)

    def to_dict(self):
        return dict(
            id=self.id,
            uuid=self.uuid,
            name=self.name,
            emailAddr= self.emailAddr,
            age= self.age,
            dob=self.dob,
            height=self.height,
            roles=self.roles,
            status=self.status
        )

