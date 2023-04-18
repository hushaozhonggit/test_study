#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/10 16:31
# @Author  : hushaozhong
# @File    : run.py
# @Software: PyCharm
import os
import time
import unittest
from base.base_setting import SetTing
from base.beautiful_report import DIYReport
RootDir = os.path.dirname(os.path.dirname(__file__))
hour = time.strftime('%Y-%m-%d', time.localtime(time.time()))

if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover(SetTing().BaseDir + '/test_cases', pattern='test*.py')
    result = DIYReport(test_suite)
    result.report(description='APP UI自动化测试demo报告', filename='report.html', report_dir=SetTing().ReportDir)
