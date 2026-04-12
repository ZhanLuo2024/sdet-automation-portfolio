from core.base_page_web import BasePage

class InventoryPage(BasePage):
    """
    SauceDemo 商品列表頁 Page Object

    登入成功後會跳轉到這個頁面
    這裡封裝了商品頁的元素定位和驗證方法
    """

    URL = "https://www.saucedemo.com/inventory.html"

    # Locators
    TITLE = "[data-test='title']"
    INVENTORY_LIST = "[data-test='inventory-list']"

    def expect_page_loaded(self) -> None:
        """
        驗證商品頁已正確載入

        同時檢查
        1. URL 是否正確跳轉
        2. 頁面標題是否位 Products
        3. 商品列表是否可見
        """
        self.expect_url(self.URL)
        self.expect_text(self.TITLE, "Products")
        self.expect_visible(self.INVENTORY_LIST)