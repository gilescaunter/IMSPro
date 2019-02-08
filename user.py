from flask_login import UserMixin
from flask_pymongo import PyMongo

class User(UserMixin):
        username = ""
        password = ""

        def get_id(self):
            return 1