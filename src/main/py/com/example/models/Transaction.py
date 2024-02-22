#
#
#
import json
import csv
from uuid import uuid4
from datetime import datetime
import random
from faker import Faker

#
class Transaction(object):

    # Class Variable
    ecommerce_website_name = None
    CITIES = {
        "IN":["Delhi", "Chennei", "Pune", "Mumbai", "Banglore"],
        "USA": ["New York", "Los Angeles", "Miami"],
        "UK": ["London", "Manchester", "Liverpool", "Oxford"],
        "JP": ["Tokyo", "Osaka", "Yokohama", "Hiroshima"]
    }
    PRODUCTS = ["Mobile", "Tablet", "Computer", "Laptop", "RAM", "TV", "Speaker", "Mouse", "Keyboard", "LDC", "Monitor", "Printer"]
    COUNTRIES = ["IN", "USA", "UK", "JP"]
    CCTYPES = ["VISA", "Master", "Amex", "RuPay"]
    SITES = ["Amazon", "Flipkart", "SnapDeal", "Myntra", "Ebay"]

    # Use __slots__ to explicitly declare all data members.
    __slots__ = ["id", "uuid", "cardType", "website",  "product", "amount", "city", "country", "addts"]

    # The init method or constructor
    def __init__(self, uuid=None):

        event_datetime = datetime.now().timestamp()
        self.addts = int(event_datetime)
        if uuid is None:
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid

    def setCardType(self, cardType):
        self.cardType = cardType

    def getCardType(self):
        return self.cardType

    def setWebsite(self, website):
        self.website = website

    def getWebsite(self):
        return self.website

    def setProduct(self, product):
        self.product = product

    def getProduct(self):
        return self.product

    def setAmount(self, amount):
        self.amount = amount

    def getAmount(self):
        return self.amount

    def setCity(self, city):
        self.city = city

    def getCity(self):
        return self.city

    def setCountry(self, country):
        self.country = country

    def getCountry(self):
        return self.country

    @staticmethod
    def random():
        t = Transaction()
        fake = Faker()
        t.id = random.randint(1000, 5000)
        t.setCardType(random.choice(Transaction.CCTYPES))
        random.choice(Transaction.SITES)
        t.setWebsite(fake.url())
        t.setProduct(random.choice(Transaction.PRODUCTS))
        t.setAmount(round(random.uniform(500.99, 25000.99), 2))

        c = random.choice(Transaction.COUNTRIES)
        random.choice(Transaction.CITIES[c])

        t.setCountry(fake.country_code())
        t.setCity(fake.city())
        return t

    @staticmethod
    def dict_to_name(obj):
        return Transaction(obj['id'])

    @staticmethod
    def name_to_dict(id):
        return Transaction.to_dict(id)

    def to_dict(self):
        return dict(
            id=self.id,
            uuid=self.uuid,
            cardtype=self.cardType,
            website=self.website,
            product=self.product,
            amount=self.amount,
            city=self.city,
            country=self.country,
            addts=self.addts
        )

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_delimited_text(self, separator):
        text_val = ""
        dict_val = self.to_dict()
        for key in ["id", "uuid", "cardtype", "website",  "product", "amount", "city", "country", "addts"]:
            text_val = text_val + str(dict_val[key]) + separator

        return text_val[:-1]
