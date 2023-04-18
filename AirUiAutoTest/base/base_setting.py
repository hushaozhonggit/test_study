#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/10 15:22
# @Author  : hushaozhong
# @File    : base.py
# @Software: PyCharm
import os
import socket
from airtest.core.settings import Settings as ST


class SetTing(object):
    ST.CVSTRATEGY = ["mstpl", "tpl", "sift", "brisk"]
    Phone = 'android://127.0.0.1:5037/384dca03?cap_method=JAVACAP&&ori_method=ADBORI&&touch_method=MAXTOUCH'
    Mom = 'android:///'
    Lei = 'android://127.0.0.1:5037/emulator-5554?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH'

    hostname = socket.gethostname()
    # ip = socket.gethostbyname(hostname)
    ip = '10.32.50.176'
    ipport = "http://" + ip + ":5000/"
    IPPortDir = ipport + 'static/reports/'
    AirReportDir = ipport + 'static/air_report'

    USERNAME = 'test'
    PSW = 'test'

    BaseDir = os.path.dirname(os.path.dirname(__file__))
    ServerDir = os.path.join(BaseDir, 'report_server\\')
    NewAirDir = ServerDir.replace('/', '\\').replace('\\', '\\\\')
    NewIPPort = ipport.replace('/', '\\').replace('\\', '\\\\')

    StaticDir = os.path.join(ServerDir, 'static\\')
    TemplateDir = os.path.join(ServerDir, 'templates\\')
    ReportDir = os.path.join(StaticDir, 'reports\\')

    DatasDir = os.path.join(StaticDir, 'test_datas\\')
    AssertDir = os.path.join(DatasDir, 'assert_images\\')
    testDir = os.path.join(DatasDir, 'test_images\\')
    LogsDir = os.path.join(StaticDir, 'logs\\')
