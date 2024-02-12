from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from work_with_db import select_dict, insert, call_proc, transaction
from sql_provider import SQLProvider
from datetime import datetime
from authentication_blueprint.access import group_required, login_required
from DBCM import DBContextManager

import os

blueprint_basket = Blueprint('bp_basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_basket.route('/start')
@group_required
@login_required
def start():
    if 'basket' not in session.keys():
        print('!')
        session['basket'] = {}
    print(session.keys())
    return redirect(url_for('bp_basket.choose'))


@blueprint_basket.route('/', methods=['GET', 'POST'])
@login_required
def choose():
    db_config = current_app.config['db_config']
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)
        return render_template('basket_show.html', item=items, basket=session['basket'],
                               bask_keys=session['basket'].keys())
    else:
        id_product = request.form.get('id_product')
        sql = provider.get('add_item.sql', id=id_product)
        item = select_dict(db_config, sql)[0]
        add_to_basket(session['basket'], item)
        if not session.modified:
            session.modified = True
        return redirect(url_for('bp_basket.choose'))


def add_to_basket(bask, item):
    if str(item['s_id']) in bask.keys():
        bask[str(item['s_id'])]['amount'] += 1
    else:
        bask[str(item['s_id'])] = {'s_name': item['s_name'], 's_price': item['s_price'], 'amount': 1}



@blueprint_basket.route('/save_order', methods=['GET', 'POST'])
@login_required
def save_order():
    order_id = None
    user_id = session['user_id']
    db_config = current_app.config['db_config']
    if 'basket' in session.keys():
        transaction(db_config, user_id, provider, session)

    else:
        redirect(url_for('bp_basket.choose'))
    if not session['basket']:
        return redirect(url_for('bp_basket.choose'))

    session['basket'] = {}
    return render_template('done.html')


@blueprint_basket.route('/sec')
@login_required
@group_required
def menu():
    session.pop('basket', None)
    return redirect(url_for('index'))


@blueprint_basket.route('/clear')
@login_required
@group_required
def clear_basket():
    session['basket'] = {}
    return redirect(url_for('bp_basket.choose'))
