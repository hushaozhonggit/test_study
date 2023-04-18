# -*- encoding=utf8 -*-
__author__ = "hushaozhong"

from airtest.core.api import *
import unittest, datetime
from base.airtest_lib import case_params, SetUpCls
from base.base_setting import SetTing


class TestMusic(SetUpCls):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @case_params(casedir=__file__, logdir='login', title='司机登录', desc='测试个体司机-司机张登录成功',
                 author='hushaozhong')
    def test_login_000(self):
        touch(Template(SetTing().testDir + "tpl1671098270722.png", record_pos=(0.376, 0.892), resolution=(1080, 2340)))
        self.poco(name="com.kyepartner.express:id/to_login", text='去登陆').click()
        self.poco(name="com.kyepartner.express:id/title_tv", text='您好，欢迎加入').wait_for_appearance()
        self.poco(name="com.kyepartner.express:id/title_tv", text='您好，欢迎加入').click()
        self.poco("com.kyepartner.express:id/rb_uat").click()
        touch([500, 500])
        self.poco("com.kyepartner.express:id/phone_input").click()
        text('15012345600', search=True, enter=False)
        time.sleep(2)
        self.poco(name='com.kyepartner.express:id/right_tv', text="获取验证码").click()
        text('123456', search=True, enter=False)
        self.poco(name="com.kyepartner.express:id/login_btn", type="android.widget.RelativeLayout").click()
        time.sleep(2)
        touch([500, 100])
        name = self.poco(name="com.kyepartner.express:id/tv_userName").get_text()
        assert_equal(name, "司机张", "断言司机名字登录成功")

    @case_params(casedir=__file__, logdir='source', title='货源刷新', desc='测试货源刷新数据出现',
                 author='hushaozhong')
    def test_source(self):
        touch(Template(r"tpl1673235873114.png", record_pos=(-0.375, 0.814), resolution=(720, 1280)))
        self.poco.swipe([0.4, 0.3], [0.4, 0.5])
        assert_not_exists(Template(r"tpl1673236453765.png", record_pos=(-0.004, 0.336), resolution=(720, 1280)),
                          "货源刷新成功出数据")

    @case_params(casedir=__file__, logdir='logout', title='司机退出登录', desc='测试个体司机-司机张退出登录',
                 author='hushaozhong')
    def test_logout_999(self):
        self.poco(name="com.kyepartner.express:id/tv_text", text="反馈举报").swipe('up')
        self.poco(name="com.kyepartner.express:id/tv_text", text="设置").click()
        self.poco(name="com.kyepartner.express:id/item_setting_logout", text="退出登录").click()
        self.poco(name='android.widget.TextView', text='确定').click()
        self.poco(name="com.kyepartner.express:id/title_tv", text='您好，欢迎加入').wait_for_appearance()
        exists(
            Template(SetTing().AssertDir + "tpl1673235288634.png", record_pos=(-0.217, -0.568), resolution=(720, 1280)))


if __name__ == '__main__':
    unittest.main()
