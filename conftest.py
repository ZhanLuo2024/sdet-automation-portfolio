import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return "https://dummyjson.com"

@pytest.fixture(scope="session")
def auth_token(base_url):
    print("\n[Setup] 正在向 Authentication Server 請求 Token...")

    # 從環境變數讀取帳密，避免硬編碼憑證
    username = os.environ.get("TEST_USERNAME")
    password = os.environ.get("TEST_PASSWORD")
    assert username and password, "請設定環境變數 TEST_USERNAME 和 TEST_PASSWORD"

    # 模擬發送 API 登入請求
    payload = {
        "username": username,
        "password": password,
    }

    response = requests.post(f"{base_url}/auth/login", json=payload)

    # 基本防錯機制
    assert response.status_code == 200, "致命錯誤： Setup 階段拿取 Token 失敗"

    # 從 Response 取出 token
    token = response.json().get("accessToken")

    # yield 把 token 交給測試腳本。腳本跑完後會回來執行 yield 後面的代碼
    yield token

    # 事後清理
    print("\n[Teardown] 測試套件執行完畢，清理 Token 狀態...")

@pytest.fixture(scope="session")
def ui_credentials():
    username = os.environ.get("UI_USERNAME")
    password = os.environ.get("UI_PASSWORD")
    assert username and password, "請設定環境變數 UI_USERNAME 和 UI_PASSWORD"
    return {"username": username, "password": password}