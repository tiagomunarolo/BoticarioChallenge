from src.db.user_model import User
from src.db.db_controller import MongoClient, PRODUCTS_COLLECTION
from src.date_utils import split_date, get_current_year_and_month

SPECIFIC_CPF = ["153.509.460-56", "15350946056"]
DEFAULT_STATUS = 'Under Validation'
STATUS_APPROVED = 'Approved'


class Product(object):

    def __init__(self, code, value, date, cpf, status=DEFAULT_STATUS):
        self.code = code
        self.value = value
        self.date = date
        self.cpf = cpf
        self.status = status if cpf not in SPECIFIC_CPF else STATUS_APPROVED
        self.cashback = None

    @staticmethod
    def get_all_products(query=None):
        return MongoClient().find_elements(collection=PRODUCTS_COLLECTION, query=query)

    @staticmethod
    def get_single_product(query=None):
        return MongoClient().find_document(collection=PRODUCTS_COLLECTION, query=query)

    def check_values(self):
        if None in [self.code, self.value, self.date, self.cpf, self.status, self.cashback]:
            return False
        return True

    def find_cashback_for_current_user(self, value=0):
        user_id = User.get_current_user()
        input_data = {}
        if user_id:
            input_data = {'user_id': user_id}
        results = MongoClient().find_elements(collection=PRODUCTS_COLLECTION, query=input_data)
        sum_value = float(value) if value else 0

        year, month = get_current_year_and_month()

        for result in results:
            product_year, product_month = split_date(result.get('date'))
            if product_month == month and product_year == year:
                sum_value += float(result.get('value', 0))

        if sum_value < 1000:
            self.cashback = 0.1
        elif 1000 <= sum_value <= 1500:
            self.cashback = 0.15
        else:
            self.cashback = 0.2

    def insert_product(self):
        user_id = User.get_current_user()
        self.find_cashback_for_current_user(value=self.value)
        input_data = {
            'code': self.code, 'value': self.value,
            'date': self.date, 'cpf': self.cpf,
            'status': self.status, 'cashback': self.cashback,
            'user_id': str(user_id) if user_id else None
        }
        _id = None
        if self.check_values():
            _id = MongoClient().insert_new_document(collection=PRODUCTS_COLLECTION, data=input_data)
        return _id
