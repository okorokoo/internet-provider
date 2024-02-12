from flask import Flask, redirect, url_for, render_template, session
import json
from blueprint_query.route import blueprint_query
from authentication_blueprint.access import authentication_blueprint, login_required
from blueprint_report.route import blueprint_report
from blueprint_basket.route import blueprint_basket


app = Flask(__name__)
with open('../db_config.json') as f:
    app.config['db_config'] = json.load(f)
with open('../access.json') as f:
    app.config['access_config'] = json.load(f)
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(authentication_blueprint, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_basket, url_prefix='/basket')

app.secret_key = 'You will never guess'


@app.route('/')
@login_required
def main_menu():
    # if session['user_group'] == 'ordinary':
    #     return render_template('main_for_ordinary.html')
    # else:
    #     return render_template('main.html')
    if session.get('user_group', None) == 'ordinary':
        return render_template('main_for_ordinary.html')
    return render_template('main.html')

@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
