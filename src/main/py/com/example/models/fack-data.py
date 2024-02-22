from faker import Faker
from random import randint
from com.example.models.Transaction import Transaction

fake = Faker("en_IN")

for _ in range(100):
    '''
    print(randint(1, 100))
    print(fake.email())
    print(fake.country())
    print(fake.name())
    print(fake.text())
    print(fake.latitude(), fake.longitude())
    print(fake.url())
    print(fake.address())
    print(str(fake.latitude()))
    print(str(fake.longitude()))
    print(fake.city())
    print(fake.postcode())
    print(fake.currency())
    print(fake.currency_code())
    print(fake.currency_name())
    '''

    transaction = Transaction.random()
    record_key = str(transaction.uuid)
    record_value = str(transaction.to_dict())
    # json.dumps() function converts a Python object into a json string.
    # record_value = json.dumps({'count': random.randint(1000, 5000)})
    print("{}\t{}".format(record_key, record_value))