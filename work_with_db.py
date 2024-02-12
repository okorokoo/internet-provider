from typing import Tuple, List

from flask import current_app, redirect, url_for

from DBCM import DBContextManager

from datetime import datetime



def select_dict(db_config, _sql:str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            products = cursor.fetchall()
            if products:
                schema = [item[0] for item in cursor.description]
                products_dict = []
                for product in products:
                    products_dict.append(dict(zip(schema, product)))
                return products_dict
            return None


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        res = cursor.callproc(proc_name, param_list)
        return res

def insert(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        result = cursor.execute(_sql)
    return result

def update(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Update cursor not found')
        result = cursor.execute(_sql)
    return result

def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def transaction(db_config, user_id, provider, session):
    with DBContextManager(db_config) as cursor:
        if cursor:
            sql = provider.get('insert_order.sql', user_id=user_id, user_date=datetime.now().strftime("%Y-%m-%d"),
                               user_time=datetime.now().strftime("%H:%M:%S"))
            cursor.execute(sql)
            order_id = cursor.lastrowid
            print("1")
            print(order_id)
            if order_id:
                for key in session['basket'].keys():
                    item = session['basket'][key]
                    sql = provider.get('insert_order_list.sql', order_id=order_id, id_product=key,
                                       product_amount=item['amount'], product_price=float(item['amount']) *
                                                                                    float(item['s_price']))
                    cursor.execute(sql)
            else:
                return redirect(url_for('bp_basket.choose'))