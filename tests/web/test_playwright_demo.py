from playwright.sync_api import Page, expect

def test_ecommerce_login(page: Page, ui_credentials):

    print("\n[動作] 準備進入測試網站...")
    # 1. 導航到網站
    page.goto("https://www.saucedemo.com/")

    # 2. 尋找畫面上的輸入框（Locator 定位器）
    page.get_by_placeholder("Username").fill(ui_credentials["username"])
    page.get_by_placeholder("Password").fill(ui_credentials["password"])

    print("[動作] 已經輸入完密碼，準備點擊...")

    # 3. 點擊按鈕 (利用 CSS selector 定位元素)
    page.locator("[data-test='login-button']").click()

    # 4. 斷言
    header_title = page.locator(".title")
    expect(header_title).to_have_text("Products")

    print("[完成] 登入成功，完美驗證")


# ------------------------------------------------------------- #
# ⭐️ 必學重點：負向測試 (Negative Testing)
# ------------------------------------------------------------- #
# 正向測試驗證「正確的輸入得到正確的結果」。
# 負向測試驗證「錯誤的輸入得到正確的錯誤處理」。
#
# 為什麼需要負向測試？
# 假設登入邏輯壞掉，任何帳密都能登入，正向測試依然會 PASS。
# 只有負向測試才能抓到「系統沒有正確拒絕非法請求」這類 Bug。
#
# 這是企業級測試框架的必要組成，缺少負向測試等於只驗證了一半。
# ------------------------------------------------------------- #

def test_ecommerce_login_with_wrong_credentials(page: Page):
    """
    負向測試：輸入錯誤帳密，驗證系統有正確拒絕並顯示錯誤訊息。

    這個測試和正向測試互補：
    - 正向測試確保「對的帳密可以進去」
    - 負向測試確保「錯的帳密進不去」
    兩個都綠才代表登入功能是完整且安全的。
    """

    print("\n[動作] 準備進入測試網站（負向測試）...")

    # 1. 導航到登入頁
    page.goto("https://www.saucedemo.com/")

    # 2. 故意填入一組不存在的錯誤帳密
    #    目的是觸發系統的錯誤處理邏輯，而不是讓登入成功
    page.get_by_placeholder("Username").fill("wrong_user")
    page.get_by_placeholder("Password").fill("wrong_password")

    print("[動作] 已輸入錯誤帳密，準備點擊登入...")

    # 3. 點擊登入按鈕
    page.locator("[data-test='login-button']").click()

    # 4. 斷言一：確認系統沒有跳轉到 Products 頁
    #    如果登入邏輯壞掉（任何帳密都能進），這個斷言就會抓到問題
    #    check_visible=False 代表只檢查 URL，不需要等待元素出現
    expect(page).to_have_url("https://www.saucedemo.com/")

    # 5. 斷言二：確認畫面上出現了正確的錯誤訊息
    #    data-test='error' 是該網站錯誤訊息元素的 CSS 屬性定位器
    #    這個斷言同時驗證了：
    #      a) 錯誤訊息元素確實存在於畫面上（可見）
    #      b) 錯誤訊息的文字內容完全符合預期
    error_message = page.locator("[data-test='error']")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Username and password do not match")

    print("[完成] 系統正確拒絕了錯誤帳密，負向測試通過")
