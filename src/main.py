import os
from flask import Flask
from flask_login import LoginManager
from src.routes.purchase_routes import products_routes
from src.routes.user_routes import configure_user_routes

template_dir = os.path.abspath('./templates')
static_folder = os.path.abspath('./static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_folder)
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
login_manager = LoginManager(app)


def main():
    products_routes(app=app)
    configure_user_routes(app=app, login_manager=login_manager)
    app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == '__main__':
    main()
