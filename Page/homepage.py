from Page.UIElements import UIElements
from Base.Base import Base


class HomePage(Base):

    def __init__(self, driver):
        Base.__init__(self, driver)

    def click_my_btn(self):
        """点击首页我按钮"""
        self.click_element(UIElements.home_my_btn_id)
