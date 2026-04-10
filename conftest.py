import os

import pytest
from dotenv import load_dotenv

from core.api_client import APIClient

# load_dotenv() 會讀取專案根目錄的 .env 檔，把裡面的 key=value 載入成環境變數。
# 這樣測試程式就能用 os.getenv() 取值，而不需要把帳密直接寫在程式碼裡。
load_dotenv()


@pytest.fixture(scope="session")
def settings():
    """
    集中讀取並驗證所有外部設定。

    scope="session" 代表這個 fixture 在整個測試執行期間只會被建立一次，
    所有測試共用同一份設定，不會重複讀取環境變數。

    在這裡做提前驗證（fail fast）是刻意的設計：
    如果環境變數沒有設好，測試應該在最開始就清楚報錯，
    而不是跑到一半才因為 None 值引發難以追蹤的錯誤。
    """
    base_url = os.getenv("BASE_URL")
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")

    assert base_url, "請先設定 BASE_URL，例如 https://dummyjson.com"
    assert username, "請先設定 TEST_USERNAME"
    assert password, "請先設定 TEST_PASSWORD"

    return {
        "base_url": base_url,
        "username": username,
        "password": password,
    }


@pytest.fixture(scope="session")
def api_client(settings):
    """
    建立一個全測試共用的 APIClient 實例。

    APIClient 封裝了所有 HTTP 請求邏輯（base URL 拼接、headers 處理等），
    測試只需要呼叫語意清楚的方法，不需要直接操作 requests 庫。
    """
    return APIClient(base_url=settings["base_url"])


@pytest.fixture(scope="session")
def auth_session(api_client, settings):
    """
    執行登入並回傳 token 與使用者資料，供需要授權的測試使用。

    scope="session" 確保整個測試套件只登入一次。
    這避免了每個測試都重複發送登入請求，減少不必要的網路開銷，
    同時也讓授權相關的 setup 邏輯集中在一個地方管理。

    回傳的 dict 包含：
    - token: Bearer token 字串，用於需要授權的 API 請求
    - user: 完整的登入回傳 payload，供需要驗證使用者資料的測試使用
    """
    login_response = api_client.login(
        username=settings["username"],
        password=settings["password"],
    )

    assert login_response.status_code == 200, "登入失敗，請檢查測試帳號或 API 狀態"

    payload = login_response.json()
    access_token = payload.get("accessToken")

    # 僅確認 status 200 是不夠的，因為 API 有可能回傳 200 但 body 格式不符預期。
    # 這裡額外確認 accessToken 欄位確實存在且有值。
    assert access_token, "登入成功但沒有拿到 accessToken，請檢查 API 回傳格式"

    return {
        "token": access_token,
        "user": payload,
    }
