#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/12 22:17
# @Author  : hushaozhong
# @File    : airtest_lib.py
# @Software: PyCharm
import os
import shutil
import time, unittest, logging
from airtest.core.api import *
from airtest.core.settings import Settings as ST
from airtest.core.helper import G, log
from base.base_setting import SetTing
from base.could_report import self_simple_report
from airtest.cli.parser import cli_setup
from run_case import RootDir
from airtest.core.android.recorder import *
from airtest.core.android.adb import *


class SetUpCls(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger("airtest")
        logger.setLevel(logging.INFO)
        if not cli_setup():
            auto_setup(devices=[SetTing().Lei, ], project_root=RootDir)
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

        adb = ADB(serialno="emulator-5554")
        cls.recorder = Recorder(adb)
        # 开启录屏
        cls.recorder.start_recording()

        wake()
        start_app('com.kyepartner.express')

    @classmethod
    def tearDownClass(cls):
        stop_app('com.kyepartner.express')
        # 结束录屏
        adb = ADB(serialno="emulator-5554")
        cls.recorder = Recorder(adb)
        cls.recorder.stop_recording(output=SetTing().ReportDir+"result.mp4")


def case_params(**kwargs):
    def outer(func):
        def inner(self):
            try:
                self_set_logdir(SetTing().LogsDir + kwargs.get('logdir'))
                self.__dict__["_start_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                data = func(self)
            except Exception as e:
                log(e, desc='出现异常了！', snapshot=True)
                raise e
            finally:
                self_simple_report(filepath=kwargs.get('casedir'), logpath=SetTing().LogsDir + kwargs.get('logdir'),
                                   output=SetTing().ReportDir + f"{kwargs.get('logdir')}_report.html",
                                   case_info={"title": kwargs.get('title'), "desc": kwargs.get('desc'),
                                              "author": kwargs.get('author')}
                                   )
                self.__dict__["_html_path"] = SetTing().IPPortDir + f"{kwargs.get('logdir')}_report.html"
                self.__dict__['_testMethodDoc'] = kwargs.get('desc')
                # while not self.poco(text=kwargs.get('initele')).exists():
                #     touch(Template(SetTing().testDir + "tpl1671098270722.png", record_pos=(0.376, 0.892),
                #                    resolution=(1080, 2340)))
            return data
        return inner
    return outer


def self_set_logdir(logdir):
    """
    设置log文件夹
    """
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.mkdir(logdir)
    ST.LOG_DIR = logdir
    G.LOGGER.set_logfile(os.path.join(ST.LOG_DIR, ST.LOG_FILE))
