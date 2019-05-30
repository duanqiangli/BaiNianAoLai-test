from Base.Base import Base
from Page.UIElements import UIElements


class LoginPage(Base):
    def __init__(self, driver):
        Base.__init__(self, driver)

    def login(self, name, passwd):
        """
        登录
        :param name: 用户名
        :param passwd: 密码
        :return:
        """
        # 输入用户名
        self.send_element(UIElements.login_account_id, name)
        # 输入密码
        self.send_element(UIElements.login_passwd_id, passwd)
        # 点击登录
        self.click_element(UIElements.login_btn_id)

    def login_close_page(self):
        """关闭登录页面"""
        # 点击关闭按钮
        self.click_element(UIElements.login_close_page_btn_id)

    def if_login_btn(self):
        """判断登录按钮是否存在的方法"""
        self.get_element(UIElements.login_btn_id)
