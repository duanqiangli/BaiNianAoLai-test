from Base.Base import Base
from Page.UIElements import UIElements


class PersonPage(Base):
    def __init__(self, driver):
        Base.__init__(self, driver)

    def get_shop_cart(self):
        """获取优惠券文本内容"""
        return self.get_element(UIElements.person_shop_cart_id).text

    def click_setting_btn(self):
        """点击设置按钮"""
        self.click_element(UIElements.person_setting_btn_id)
