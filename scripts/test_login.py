import sys, os
import pytest


sys.path.append(os.getcwd())

from Base.getdriver import get_phone_driver
from Page.Page import Page
from Base.getfiledata import GetFileData
from selenium.common.exceptions import TimeoutException


# {"suc":[()], "fail":[()]}
def get_login_data():
    # 预期成功列表
    suc_list = []
    # 预期失败列表
    fail_list = []
    # 读取yaml数据
    login_data = GetFileData().get_yaml_data("logindata.yml")
    for i in login_data:
        if login_data.get(i).get("toast"):
            # 预期失败测试用例 case_num, account, passwd, toast, exp_data
            fail_list.append((i, login_data.get(i).get("account"), login_data.get(i).get("passwd"),
                              login_data.get(i).get("toast"), login_data.get(i).get("expect_data")))
        else:
            # 预期成功测试用例 case_num, account, passwd, exp_data
            suc_list.append((i, login_data.get(i).get("account"), login_data.get(i).get("passwd"),
                             login_data.get(i).get("expect_data")))
    return {"suc": suc_list, "fail": fail_list}


class TestLogin:
    def setup_class(self):
        # 初始化driver
        self.driver = get_phone_driver("com.yunmall.lc", "com.yunmall.ymctoc.ui.activity.MainActivity")
        # 初始化统一入口类
        self.page_obj = Page(self.driver)

    def teardown_class(self):
        # 退出driver对象
        self.driver.quit()
    @pytest.fixture(autouse= True)
    def go_to_login(self):
        """进入登录页的方法"""
        # 点击我
        self.page_obj.get_homepage().click_my_btn()
        # 点击已有账号
        self.page_obj.get_signpage().click_exits_account()


    @pytest.mark.parametrize("case_num, account, passwd, exp_data", get_login_data().get("suc"))
    def test_login_suc(self, case_num, account, passwd, exp_data):
        """

        :param case_num: 用例编号
        :param account: 用户名
        :param passwd: 密码
        :param exp_data: 预期结果
        :return:
        """

        # 登录操作 --个人中心
        self.page_obj.get_loginpage().login(account, passwd)
        try:
            # 获取我的优惠
            shop_cart = self.page_obj.get_personpage().get_shop_cart()
            try:
                assert exp_data == shop_cart
            except AssertionError:
                """停留在个人中心，需要执行退出操作"""
                # 截图
                self.page_obj.get_loginpage().screen_page()
                assert False
            finally:
                # 点击设置
                self.page_obj.get_personpage().click_setting_btn()
                # 退出操作
                self.page_obj.get_settingpage().logout()
        except TimeoutException:
            # 截图
            self.page_obj.get_loginpage().screen_page()
            # 关闭页面
            self.page_obj.get_loginpage().login_close_page()
            assert False

    @pytest.mark.parametrize("case_num, account, passwd, toast, exp_data", get_login_data().get("fail"))
    def test_login_fail(self, case_num, account, passwd, toast, exp_data):
        """

        :param case_num: 用例编号
        :param account: 用户名
        :param passwd: 密码
        :param toast: 获取toast消息参数
        :param exp_data: 预期结果
        :return:
        """
        self.page_obj.get_loginpage().login(account, passwd)
        try:
            # 获取toast消息
            toast_data = self.page_obj.get_homepage().get_toast(toast)
            try:
                # 先判断登录在不在
                self.page_obj.get_loginpage().if_login_btn()
                # 登录存在再进行断言
                assert toast_data == exp_data
                # 断言成功，在登录页退出
                self.page_obj.get_loginpage().login_close_page()
            except TimeoutException:
                # 获取到了toast，但进入了个人中心页
                # 截图
                self.page_obj.get_loginpage().scroll_sreen()
                # 退出
                self.page_obj.get_personpage().click_setting_btn()
                self.page_obj.get_settingpage().logout()
                # 抛出断言错误
                assert False

            except AssertionError:
                    # 截图
                    self.page_obj.get_loginpage().scroll_sreen()
                    # 退出
                    self.page_obj.get_loginpage().login_close_page()
                    # 抛出断言错误
                    assert False

        except TimeoutException:
            try:
                # 获取登录按钮
                self.page_obj.get_loginpage().if_login_btn()
                # 关闭登录页面
                self.page_obj.get_loginpage().login_close_page()
            except TimeoutException:
                # 截图
                self.page_obj.get_settingpage().scroll_sreen()
                # 执行从个人中心页退出的方法
                self.page_obj.get_personpage().click_setting_btn()
                self.page_obj.get_settingpage().logout()

                assert False
