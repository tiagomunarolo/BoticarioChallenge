import requests
from bson import ObjectId
from src.db.user_model import User, USERS_COLLECTION
from src.db.db_controller import MongoClient


def get_cashback():
    user_id = User.get_current_user()
    user_info = MongoClient().find_document(collection=USERS_COLLECTION, query={'_id': ObjectId(user_id)})
    cpf = user_info.get('cpf')

    cpf_formatted = cpf.replace('.', '').replace('-', '')
    url = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback?cpf={}'.format(cpf_formatted)
    headers = {'token': 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm'}
    response = requests.get(url, headers=headers, verify=False)

    if response.status_code != 200:
        return None
    json_body = response.json()
    credit = json_body.get('body').get('credit')
    return credit
