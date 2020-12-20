from flask import request, render_template, redirect, url_for
from flask_login import login_required
from src.api.cashback_api import get_cashback
from src.db.user_model import User
from src.db.product_model import Product


def products_routes(app):
    @app.route('/products', methods=['POST'])
    @login_required
    def insert_product():
        if request.form.get('submit', None):
            code = request.form.get('code', None)
            value = request.form.get('value', None)
            date = request.form.get('date', None)
            cpf = request.form.get('cpf', None)

            product = Product(code=code, value=value, date=date, cpf=cpf)
            product_id = product.insert_product()
            if product_id:
                app.logger.info('Product inserted sucessfully')
                return redirect(url_for('get_products'))

        app.logger.info('Product insertion failed')
        return render_template('order.html')

    @app.route('/products', methods=['GET'])
    @login_required
    def get_products():
        if request.args.get('register'):
            app.logger.info('Requested to add new products')
            return render_template('order.html')

        query = {}
        user_id = User.get_current_user()
        if user_id:
            query = {'user_id': user_id}
        products = list(Product.get_all_products(query=query))
        app.logger.info('Total products associated to user: {}'.format(len(products)))
        return render_template('products_list.html', products=products)

    @app.route('/cashback', methods=['GET'])
    @login_required
    def get_cashback_api():
        app.logger.info('Api called')
        cashback = get_cashback()
        app.logger.info('{}'.format(cashback))
        return render_template('cashback.html', cashback_value=cashback)
