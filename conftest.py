import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "https://dummyjson.com"

@pytest.fixture(scope="session")
def auth_token():
    print("\n[Setup] 正在向 Authentication Server 請求 Token...")

    # 摸你發送 API 登入請求
    payload = {
        "username": "emilys",
        "password": "emilyspass",
    }

    response = requests.post("https://dummyjson.com/auth/login", json=payload)

    # 基本防錯機制
    assert response.status_code == 200, "致命錯誤： Setup 階段拿取 Token 失敗"

    # 從 Response 取出 token
    token = response.json().get("accessToken")

    # yield 把 token 交給測試腳本。腳本跑完後會回來執行 yield 後面的代碼
    yield token

    # 事後清理
    print("\n[Teardown] 測試套件執行完畢，清理 Token 狀態...")