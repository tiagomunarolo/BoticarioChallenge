# BoticarioChallange
Desafio Boticario

# How it works:
- It is a project, using Python as backend, Flask as web-service and Mongo as database.
- User acces is controlled via flask_login, controlling access to some routes and checking if user is authorized.
- All passwords are stored inside Mongo using encryption
- Frontend/UI using simple Html code, Bootstrap 4 and Jinja templates

# Actions:
- User can create a new account (if email is not registered yet)
- User can sign-in
- User can logout
- User can see all their purchases
- User can register a new purchase
- Authentication is checked in every endpoint (restricted access)
- Cashback is computed based on all purchases of current user and according to current month (bonification criteria)
- User can see total cashback (returned from API)

# Requisites:
- Python 3.6+
- MongoDb installed locally and running ("mongod in terminal")
- Install python modules listed inside requirements.txt

# Steps:
- 1: Create Virtualenv for Python (Ex: pyenv virtualenv 3.6.5 boticario)
- 2: Activate venv (Ex: pyenv activate boticario)
- 3: Install requirements: pip install -r requirements.txt
- 4: Run main.py (Tested using Pycharm) or run from terminal adding project root to PYTHONPATH (ex: export PYTHONPATH="${PYTHONPATH}:/Users/tiago/PycharmProjects/BoticarioChallange")
and then: python src/main.py -> Working dir should be Project root (Ex: /Users/tiago/PycharmProjects/BoticarioChallange)


# External API
- Check src/api. Used HTTPS requests (GET) and provided Token to pass a "CPF" and then retrieve a generic number representing cashback value.
It is assumed that CPF is the same as the registered during Signup. Some logs were implemented to show app status.

# Routes:
- Check src/routes