import os
from flask import Blueprint, render_template, request, current_app
from work_with_db import select_dict
from sql_provider import SQLProvider
from authentication_blueprint.access import login_required, group_required

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates2')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


#новое
@blueprint_query.route('/query_menu', methods = ['GET', 'POST'])
def start_index():
    return render_template("main.html")


@blueprint_query.route('/result', methods=['GET', 'POST'])
@group_required
def query_index():
    if request.method == 'GET':
        return render_template('input_param.html')
    else:
        category = request.form.get('category')
        price = request.form.get('price')
        name1 = request.form.get('name')
        _sql = None  # Инициализируем _sql как None

        if category and price:
            _sql = provider.get('request4.sql', category=category, price=price)
        elif category and name1:
            _sql = provider.get('product_category_name.sql', category=category, name1=name1)
        elif price and name1:
            _sql = provider.get('product_price_name.sql', price=price, name1=name1)
        elif category:
            _sql = provider.get('product_category.sql', category=category)
        elif price:
            _sql = provider.get('product_price.sql', price=price)
        elif name1:
            _sql = provider.get('product_name.sql', name1=name1)
        else:
            return render_template('no_result.html')
        if _sql is not None:
            products = select_dict(current_app.config['db_config'], _sql)
            if products:
                prod_title = 'Результаты запроса'
                return render_template('dynamic_request3.html', products=products, prod_title=prod_title)
            else:
                return render_template('no_result.html')

@blueprint_query.route('/the_youngest_client', methods=['GET'])
@group_required
def query1_index():
    # SQL-запрос для выбора самого дорогого продукта
    _sql = provider.get('request3.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    if products:
        prod_title = 'Сведения о самом молодом клиенте компании'
        return render_template('dynamic_request3.html', products=products, prod_title=prod_title)
    else:
        return render_template('no_result.html')

@blueprint_query.route('/the biggest expenses', methods=['GET'])
@group_required
def query2_index():
    # SQL-запрос для выбора самого дешёвого продукта
    _sql = provider.get('request6.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    if products:
        prod_title = 'Сведения о клиенте/ах, наиболее активно расходовавших баланс в марте 2020 года'
        return render_template('dynamic_request6.html', products=products, prod_title=prod_title)
    else:
        return render_template('no_result.html')


@blueprint_query.route('/balance_never_changed', methods=['GET'])
@group_required
def query4_index():
    # SQL-запрос для выбора самого дорогого продукта
    _sql = provider.get('request4.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    if products:
        prod_title = 'Сведения о клиентах, которые ни разу не изменяли баланс'
        return render_template('dynamic_request4.html', products=products, prod_title=prod_title)
    else:
        return render_template('no_result.html')
