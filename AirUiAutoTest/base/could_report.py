#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/10 22:04
# @Author  : hushaozhong
# @File    : could_report.py
# @Software: PyCharm
import json
import os
from airtest.cli.info import get_script_info
from airtest.report.report import LogToHtml
from airtest.utils.compat import script_dir_name
from airtest.core.settings import Settings as ST
from base.base_setting import SetTing


class DIYLogToHtml(LogToHtml):

    def __init__(self, script_root, log_root="", static_root="", export_dir=None, script_name="", logfile=None,
                 lang="en", plugins=None):
        super().__init__(script_root, log_root, static_root, export_dir, script_name, logfile, lang, plugins)
        self.log = []
        self.script_root = script_root
        self.script_name = script_name
        if not self.script_name or os.path.isfile(self.script_root):
            self.script_root, self.script_name = script_dir_name(self.script_root)
        self.log_root = log_root or ST.LOG_DIR or os.path.join(".", "log")
        self.static_root = static_root or SetTing().AirReportDir
        self.test_result = True
        self.run_start = None
        self.run_end = None
        self.export_dir = export_dir
        self.logfile = logfile or getattr(ST, "LOG_FILE", "log")
        self.lang = lang
        self.init_plugin_modules(plugins)

    def report_data(self, output_file=None, record_list=None, case_info=None):
        """
        """
        if case_info is None:
            case_info = {}
        self._load()
        steps = self._analyse()

        script_path = os.path.join(self.script_root, self.script_name)
        info = json.loads(get_script_info(script_path))
        info['title'] = case_info.get('title', '')
        info['author'] = case_info.get('author', '')
        info['desc'] = case_info.get('desc', '')

        if record_list:
            records = [os.path.join("log", f) if self.export_dir
                       else os.path.abspath(os.path.join(self.log_root, f)) for f in record_list]
        else:
            records = []

        if not self.static_root.endswith(os.path.sep):
            self.static_root = self.static_root.replace("\\", "/")
            self.static_root += "/"

        if not output_file:
            output_file = "log.html"

        data = {}
        data['steps'] = steps
        data['name'] = self.script_root
        data['scale'] = self.scale
        data['test_result'] = self.test_result
        data['run_end'] = self.run_end
        data['run_start'] = self.run_start
        data['static_root'] = self.static_root
        data['lang'] = self.lang
        data['records'] = records
        data['info'] = info
        data['log'] = self.get_relative_log(output_file)
        data['console'] = self.get_console(output_file)
        # 如果带有<>符号，容易被highlight.js认为是特殊语法，有可能导致页面显示异常，尝试替换成不常用的{}
        info = json.dumps(data).replace("<", "{").replace(">", "}")
        info = info.replace(SetTing().NewAirDir, SetTing().NewIPPort)
        data['data'] = info
        return data

    def report(self, template_name="air_template.html", output_file="log.html",
               record_list=None, case_info=None):
        """
        """
        if case_info is None:
            case_info = {}
        if not self.script_name:
            path, self.script_name = script_dir_name(self.script_root)

        if self.export_dir:
            self.script_root, self.log_root = self._make_export_dir()
            # output_file可传入文件名，或绝对路径
            output_file = output_file if output_file and os.path.isabs(output_file) \
                else os.path.join(self.script_root, output_file or "log.html")
            if not self.static_root.startswith("http"):
                self.static_root = "static/"

        if not record_list:
            record_list = [f for f in os.listdir(self.log_root) if f.endswith(".mp4")]
        data = self.report_data(output_file=output_file, record_list=record_list, case_info=case_info)
        return self._render(template_name, output_file, **data)


def self_simple_report(filepath, logpath=True, logfile=None, output="log.html", case_info=None):
    if case_info is None:
        case_info = {}
    path, name = script_dir_name(filepath)
    if logpath is True:
        logpath = os.path.join(path, getattr(ST, "LOG_DIR", "log"))
    rpt = DIYLogToHtml(path, logpath, logfile=logfile or getattr(ST, "LOG_FILE", "log.txt"), script_name=name,
                       lang="zh", plugins=['poco.utils.airtest.report'])
    rpt.report("air_template.html", output_file=output, case_info=case_info)
