from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from work_with_db import select_dict, call_proc, select
import os
from sql_provider import SQLProvider
from authentication_blueprint.access import group_required, login_required


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


report_list = [
    {'rep_name':'Отчёт 1 ', 'rep_id':'1'},
    {'rep_name':'Отчёт 2', 'rep_id':'2'},
]
report_url = {
    '1': {'create_rep':'bp_report.create_rep1', 'view_rep':'bp_report.view_rep1'},
    '2': {'create_rep':'bp_report.create_rep2', 'view_rep':'bp_report.view_rep2'}
}


@blueprint_report.route('/', methods=['GET', 'POST'])
def start_report():
    if request.method == 'GET':
        if session['user_group'] == 'manager':
            return render_template('menu_report_manager.html', report_list=report_list)
        return render_template('menu_report.html', report_list=report_list)
    else:
        rep_id = request.form.get('rep_id')
        print('rep_id = ', rep_id)
        if request.form.get('create_rep'):
            url_rep = report_url[rep_id]['create_rep']
        else:
            url_rep = report_url[rep_id]['view_rep']
        print('url_rep = ', url_rep)
        return redirect(url_for(url_rep))
    # из формы получает номер отчета и какую кнопку


@blueprint_report.route('/create_rep1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        print("GET_create")
        return render_template('report_create.html')
    else:
        print(current_app.config['db_config'])
        print("POST_create")
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print("Loading...")
        if rep_year and rep_month:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            print(product_result, schema)
            if product_result:
                return "Такой отчёт уже существует"
            else:
                res = call_proc(current_app.config['db_config'], 'sum_cost2', rep_month, rep_year)
                print('res=', res)
                return render_template('report_created.html')
        else:
            return "Repeat input"




@blueprint_report.route('/view_rep1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('view_rep.html')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print(rep_month)
        print(rep_year)
        if rep_year and rep_month:
            _sql = provider.get('rep1.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return render_template('result_rep1.html', schema=["ID услуги", "Кол-во", "Стоимость"], result=product_result, year=rep_year, month=rep_month)
            else:
                return "Такой отчёт не был создан"
        else:
            return "Repeat input"


@blueprint_report.route('/create_rep2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        print("GET_create2")
        return render_template('report_create.html')
    else:
        print(current_app.config['db_config'])
        print("POST_create")
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print(rep_month)
        print(rep_year)
        print("Loading...")
        if rep_year and rep_month:
            _sql = provider.get('rep2.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return "Такой отчёт уже существует"
            else:
                res = call_proc(current_app.config['db_config'], 'revenue', rep_month, rep_year)
                print('res=', res)
                return render_template('report_created.html')
        else:
            return "Repeat input"


@blueprint_report.route('/view_rep2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    if request.method == 'GET':
        return render_template('view_rep2.html')
    else:
        rep_month = request.form.get('input_month')
        rep_year = request.form.get('input_year')
        print(rep_month)
        print(rep_year)
        if rep_year and rep_month:
            _sql = provider.get('rep2.sql', in_year=rep_year, in_month=rep_month)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if product_result:
                return render_template('result_rep2.html',
                                       schema=["Выручка"],
                                       result=product_result, year=rep_year, month=rep_month)
            else:
                return "Такой отчёт не был создан"
        else:
            return "Repeat input"


# @blueprint_report.route('/')
# @group_required
# @login_required
# def report():
#     if session['user_group'] == 'manager':
#         return render_template('choose_manager.html')
#     return render_template('choose.html')
#
#
# @blueprint_report.route('/create', methods=['GET', 'POST'])
# @group_required
# @login_required
# def report_create():
#     if request.method == 'GET':
#         return render_template('otchet_in.html')
#     else:
#         year = request.form.get('in_date')
#         month = request.form.get('out_date')
#         _sql = provider.get('check_rep.sql', date_start=year, date_end=month)
#         cost = select_dict(current_app.config['db_config'], _sql)
#         print(cost)
#         if cost:
#             prod_title = 'Данный отчет уже существует'
#             return render_template('dynamic_otchet.html', products=cost, prod_title=prod_title)
#         else:
#             # _sql = provider.get('gen_report.sql', in_date=start, out_date=end)
#             cost = call_proc(current_app.config['db_config'], 'sum_cost', year, month)
#             # cost = select_dict(current_app.config['db_config'], _sql)
#             _sql = provider.get("print_last.sql", date_start=year, date_end=month)
#             res = select_dict(current_app.config['db_config'], _sql)
#             prod_title = "Отчет успешно создан"
#             return render_template('dynamic_otchet.html', products=res, prod_title=prod_title)
#
#
# @blueprint_report.route('/check', methods=['GET', 'POST'])
# @group_required
# @login_required
# def check_reports():
#     _sql = provider.get("date_get.sql")
#     res = select_dict(current_app.config['db_config'], _sql)
#     if res:
#         prod_title = 'Результат'
#         return render_template('dynamic_otchet.html', products=res, prod_title=prod_title)