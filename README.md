# BoticarioChallange
Desafio Boticario


# How it works:
- It is a project, using Python as backend, Flask as web-service and Mongo as database.
- User acces is controlled via flask_login, controlling access to some routes and checking if user is authorized.
- All passwords are stored inside Mongo using encryption
- Frontend/UI using simple Html code and Bootstrap 4



# Requisites:
- Python 3.6+
- MongoDb installed locally and running ("mongod in terminal")
- Install python modules listed inside requirements.txt

# Steps:
- 1: Create Virtualenv for Python (Ex: pyenv virtualenv 3.6.5 boticario)
- 2: Activate venv (Ex: pyenv activate boticario)
- 3: Install requirements: pip install -r requirements.txt
- 4: Run main.py (Tested using Pycharm) or run from terminal adding project root to PYTHONPATH (ex: export PYTHONPATH="${PYTHONPATH}:/Users/tiago/PycharmProjects/BoticarioChallange")
and the: python src/main.py -> Working dir should be Project root (Ex: /Users/tiago/PycharmProjects/BoticarioChallange)

# Routes:
- Check src/routes