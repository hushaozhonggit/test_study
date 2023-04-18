# -*- encoding=utf8 -*-
__author__ = "590156"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/emulator-5554?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH",])


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


poco(text="确定")poco("android.widget.FrameLayout").offspring("android:id/content").offspring("com.kyepartner.express:id/layout_button_container").child("android.widget.RelativeLayout")[1]
# script content
print("start...")
exists(Template(r"tpl1673235288634.png", record_pos=(-0.217, -0.568), resolution=(720, 1280)))
touch(Template(r"tpl1673235873114.png", record_pos=(-0.375, 0.814), resolution=(720, 1280)))
assert_not_exists(Template(r"tpl1673236453765.png", record_pos=(-0.004, 0.336), resolution=(720, 1280)), "请填写测试点")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)