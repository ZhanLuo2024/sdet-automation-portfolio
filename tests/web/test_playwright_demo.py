from playwright.sync_api import Page, expect

def test_ecommerce_login(page: Page):

  print("\n[動作] 準備進入測試網站...")
  # 1. 導航到網站
  page.goto("https://www.saucedemo.com/")

  # 2. 尋找畫面上的輸入框（Locator 定位器）
  page.get_by_placeholder("Username").fill("standard_user")
  page.get_by_placeholder("Password").fill("secret_sauce")

  print("[動作] 已經輸入完密碼，準備點擊...")

  # 3. 點擊按鈕 (利用 CSS selector 定位元素)
  page.locator("[data-test='login-button']").click()

  # 4. 斷言
  header_title = page.locator(".title")
  expect(header_title).to_have_text("Products")

  print("[完成] 登入成功，完美驗證")