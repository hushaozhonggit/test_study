#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/11 12:52
# @Author  : hushaozhong
# @File    : service.py
# @Software: PyCharm
from flask import Flask, session, url_for, request, render_template
from werkzeug.utils import redirect
from base.base_setting import SetTing
from run_case import hour

app = Flask(__name__)
app.secret_key = 'dasfdsfsfds'
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    username = session.get('username')
    if username == SetTing().USERNAME:
        return app.send_static_file('reports/report.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    else:
        username = request.form.get('username')
        if username == SetTing().USERNAME:
            password = request.form.get('password')
            if password == SetTing().PSW:
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('/login.html', errmsg='密码错误')
        else:
            return render_template('/login.html', errmsg='用户名错误')


@app.route('/favicon.ico')
def get_favi():
    return app.send_static_file('air_report/images/favicon.jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)