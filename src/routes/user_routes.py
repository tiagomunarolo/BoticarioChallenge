from flask import flash
from flask import render_template, request, redirect, url_for
from flask_login import login_required, logout_user, login_user
from src.constants import CREATE_ACCOUNT, LOGIN
from src.db.user_model import User


def configure_user_routes(app, login_manager):
    @app.route('/home', methods=['POST', 'GET'])
    def authenticate_user():
        user_email = request.form.get('email', None)
        user_psw = request.form.get('password', None)
        if user_email and user_psw:
            user = User(email=user_email, password=user_psw)
            is_user_auth = user.is_authenticated()
            if is_user_auth:
                app.logger.info('user authorized...redirecting')
                login_user(user, remember=False)
                return redirect(url_for('execute_login'))
            else:
                app.logger.info('email/Psw incorrect')
                flash('User email and/or password is incorrect!')

        return render_template('home.html')

    @app.route('/register', methods=['POST', 'GET'])
    def register_new_user():
        if request.method == 'POST' and request.form.get('submit', None):
            user_psw = request.form.get('password', None)
            confirm_psw = request.form.get('confirm_password', None)

            if None in request.form.values():
                flash('Please, fill all required fields!')
                return render_template('register.html')

            cpf = request.form.get('cpf', None)
            cpf = cpf.replace('.', '').replace('-', '') if cpf else None
            if cpf and not cpf.isdigit():
                flash('CPF should be just numbers! Please, try again...')
                return render_template('register.html')

            if confirm_psw != user_psw:
                flash('Password does not match! Please, try again...')
                return render_template('register.html')

            user_created = User(kwargs=request.form).register_user()
            if user_created:
                app.logger.info('Account created')
                flash(' Account Created Successfully!')
            else:
                app.logger.info('This email and/or cpf is in use. Please, register with a new one!')
                flash('This email and/or cpf is in use. Please, register with a new one!')
            return render_template('home.html')

        return render_template('register.html')

    @app.route('/', methods=['GET', 'POST'])
    def home_page():
        if request.method == 'POST':
            submit_action = request.form.get('submit', None)
            if submit_action == CREATE_ACCOUNT:
                app.logger.info('Redirecting to register_new_user')
                return redirect(url_for('register_new_user'), code=307)
            elif submit_action == LOGIN:
                app.logger.info('Redirecting to authenticate_user')
                return redirect(url_for('authenticate_user', data=request.form), code=307)

        return render_template('register.html')

    @app.route('/order')
    @login_required
    def execute_login():
        return render_template('order.html')

    @app.route("/logout", methods=["GET"])
    @login_required
    def logout():
        """Logout the current user."""
        logout_user()
        app.logger.info('User logout done!')
        return redirect(url_for('home_page'))

    @login_manager.user_loader
    def load_user(user_id):
        app.logger.info('{}'.format(user_id if user_id else 'No user_id found'))
        return User.searchid(user_id)
