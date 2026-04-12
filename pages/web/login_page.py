from core.base_page_web import BasePage

class LoginPage(BasePage):
    """
    SauceDemo 登入頁的 Page Object

    所有和登入頁相關的元素定位，操作，斷言都封裝在這裡
    如果登入頁的 UI 改變（例如按鈕的 selector）
    只需要修改這個 class 
    """

    URL = "https://www.saucedemo.com/"

    # Locators - 集中定於，方便維護
    USERNAME_INPUT = "[data-test='username']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BUTTON = "[data-test='login-button']"
    ERROR_MESSAGE = "[data-test='error']"

    def open(self):
        """導航到登入頁"""
        self.navigate(self.URL)
        return self
    
    def login(self, username: str, password: str):
        """
        執行完整的登入流程：填寫帳密 -> 點擊登入

        登入成功回傳 InventoryPage 實例
        模擬「登入後跳轉到商品頁」的真實行為
        """
        from pages.web.inventory_page import InventoryPage

        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return InventoryPage(self.page)
    
    def login_with_invalid_credentials(self, username: str, password: str):
        """
        執行登入但預期會失敗，不回傳新頁面

        用於負向測試：填入錯誤帳密後，頁面應該留在登入頁
        """
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        return self
    
    def expect_error_message(self, expected_text: str) -> None:
        """斷言登入錯誤訊息包含預期文字"""
        self.expect_visible(self.ERROR_MESSAGE)
        self.expect_text(self.ERROR_MESSAGE, expected_text)

    def expect_still_on_login_page(self) -> None:
        """斷言頁面沒有跳轉，仍然停在登入頁"""
        self.expect_url(self.URL)