from flask_login import UserMixin, current_user
from src.db.db_controller import MongoClient, USERS_COLLECTION
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin):

    def __init__(self, auth_required=True, **kwargs):
        kwargs = kwargs if 'kwargs' not in kwargs else kwargs.get('kwargs')
        password = kwargs.get('password', None)
        self.password = password
        self._id = kwargs.get('_id', None)
        self.email = kwargs.get('email', None)
        self.cpf = kwargs.get('cpf', None)
        self.full_name = kwargs.get('full_name', None)
        self.authenticated = self._check_authentication(
            password) if password and auth_required else not auth_required

        self.check_user_by_id(self._id)

    @staticmethod
    def _get_password_hash(stored_psw, psw_received):
        return check_password_hash(stored_psw, psw_received)

    @staticmethod
    def _generate_password_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def searchid(_id):
        user = MongoClient().find_document(collection=USERS_COLLECTION, query={'_id': ObjectId(_id)})
        return User(auth_required=False, kwargs=user if user else {})

    @staticmethod
    def get_current_user():
        if current_user and current_user._id:
            return current_user._id
        elif current_user and current_user.email:
            user = MongoClient().find_document(collection=USERS_COLLECTION, query={'email': current_user.email})
            return str(user.get('_id'))
        return None

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self._id

    def register_user(self):
        self.password = self._generate_password_hash(self.password)
        data = {'email': self.email, 'password': self.password, 'cpf': self.cpf, 'full_name': self.full_name}
        user_found = MongoClient().find_document(collection=USERS_COLLECTION, query={'email': self.email})
        if not bool(user_found):
            user_id = MongoClient().insert_new_document(collection=USERS_COLLECTION, data=data)
            self._id = user_id if user_id else self._id
            return self._id
        return False

    def check_user_by_id(self, _id):
        if not _id:
            return False
        user = MongoClient().find_document(collection=USERS_COLLECTION, query={'_id': ObjectId(_id)})
        if user:
            self._id = str(user.get('_id'))
        return bool(user)

    def _check_authentication(self, password):
        user = MongoClient().find_document(collection=USERS_COLLECTION, query={'email': self.email})
        if not user:
            return False

        self.password = self._generate_password_hash(password)
        password_match = self._get_password_hash(stored_psw=user.get('password'), psw_received=password)
        if not password_match:
            return False

        self._id = str(user.get('_id'))
        return self._id
