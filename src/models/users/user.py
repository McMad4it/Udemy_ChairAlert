import uuid
from Section5.src.common.utils import Utils
from Section5.src.common.database import Database
from Section5.src.models.alerts.alert import Alert
import Section5.src.models.users.errors as UserErrors
import Section5.src.models.users.constants as UserConstants

__author__ = 'neil'


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        '''
        THis method verifies that email/password combo (as sent by the site forms) is valid or not.
        Checks that the email exists, and that the password associated to that email is correct.
        :param email: The user's email
        :param password:  The sha512 hashed password
        :return: True if valid, false otherwise
        '''

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})  # Password in sha512 -> pbkdf2_sha512

        if user_data is None:  # Tell the user that their email doesn't exist
            raise UserErrors.UserNotExistsError("This user does not exist.")

        if not Utils.check_hashed_password(password, user_data['password']):  # User email address is not formatted properly.
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        '''
        This method registers a user using email and password.
        The password already comes hashed as sha-512
        :param email: user's e-mail (might be invalid)
        :param password: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        '''

        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        if user_data is not None:  # user data exists in database therefore user exists.
            raise UserErrors.UserAlreadyRegistered("The user already exists")

        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email address you have provided is not valid")

       # no exceptions raised then the user is registered in the database.
        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
