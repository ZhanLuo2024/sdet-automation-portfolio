import pytest

from pages.web.login_page import LoginPage


@pytest.mark.web
@pytest.mark.smoke
def test_login_success(page, ui_credentials, screenshot_on_failure):
    """
    正向測試： 使用正確的帳密登入，驗證成功跳轉商品頁

    這個測試完全不知道登入按鈕的 selector 是什麼
    所有操作都透過 LoginPage 和 InventoryPage 完成
    """
    login_page = LoginPage(page)
    login_page.open()

    inventory_page = login_page.login(
        username=ui_credentials["username"],
        password=ui_credentials["password"],
    )

    inventory_page.expect_page_loaded()

@pytest.mark.web
@pytest.mark.regression
def test_login_with_wrong_credentials(page, screenshot_on_failure):
    """
    負向測試：使用錯誤的帳密登入，驗證系統正確拒絕

    驗證兩件事：
    1. 頁面沒有跳轉
    2. 畫面出現正確的錯誤訊息
    """
    login_page = LoginPage(page)
    login_page.open()

    login_page.login_with_invalid_credentials(
        username="wrong_user",
        password="wrong_password",
    )

    login_page.expect_still_on_login_page()
    login_page.expect_error_message(
        "Epic sadface: Username and password do not match any user in this service"
    )