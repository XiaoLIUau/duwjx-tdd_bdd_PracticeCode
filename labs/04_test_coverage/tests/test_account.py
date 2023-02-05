"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_represent_as_string(self):
        """ Test Account name represented as a string """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(str(account),'<Account %r>' % data["name"])

    def test_to_dic(self):
        """ Test Account to dictionary """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        output = account.to_dict()
        self.assertEqual(output["name"], account.name)
        self.assertEqual(output["email"], account.email)
        self.assertEqual(output["phone_number"], account.phone_number)
        self.assertEqual(output["disabled"], account.disabled)
        self.assertEqual(output["date_joined"],account.date_joined)

    def test_from_dic(self):
        """ Test Account from dictionary """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account()
        account.from_dict(data)
        self.assertEqual(data["name"], account.name)
        self.assertEqual(data["email"], account.email)
        self.assertEqual(data["phone_number"], account.phone_number)
        self.assertEqual(data["disabled"], account.disabled)

    def test_update_an_account(self):
        """ Test Account update"""
        name_update = 'Boo'
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account_id = account.id
        result = account.find(account_id)
        self.assertNotEqual(result.name, name_update)
        account.name = name_update
        account.update()
        result = account.find(account_id)
        self.assertEqual(result.name, name_update)

    def test_update_without_id(self):
        """ Test Account update without id """
        name_update = 'Boo'
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertNotEqual(account.name, name_update)
        account.name = name_update
        account.id = None
        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """ Test Account deletion """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_find_account_by_id(self):
        """ Test find account using id """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account_id = account.id
        result = account.find(account_id)
        self.assertEqual(result.name,data['name'])
