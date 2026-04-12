from playwright.sync_api import Page, expect


class BasePage:
    """
    所有 web Page Object 的基類

    封裝 Playwright 的通用操作（導航，點擊，填寫，斷言）
    子類只需要定義自己的 locator 和業務方法
    不需要重複處理底層頁面互動邏輯

    如果 Playwright 的 API 變動，或者需要加入統一的等待策略
    只需要修改這裡，所有繼承它的 Page Object 自動生效
    """

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """導航到指定 URL"""
        self.page.goto(url)

    def click(self, selector: str) -> None:
        """點擊指定元素 Playwright 會自動等待元素可互動後才執行"""
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        """在指定輸入框中填入"""
        self.page.locator(selector).fill(text)

    def get_text(self, selector: str) -> str:
        """取得指定元素的文字內容"""
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        """檢查指定元素是否可見"""
        return self.page.locator(selector).is_visible()

    def expect_text(self, selector: str, expected: str) -> None:
        """斷言指定元素的文字內容符合預期"""
        expect(self.page.locator(selector)).to_have_text(expected)

    def expect_visible(self, selector: str) -> None:
        """斷言指定元素在畫面上可見"""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_url(self, url: str) -> None:
        """斷言當前頁面的URL是否符合預期"""
        expect(self.page).to_have_url(url)
