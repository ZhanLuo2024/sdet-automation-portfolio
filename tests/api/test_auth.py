import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_login_returns_access_token(auth_session):
    """
    這個測試在檢查一件最重要的事：
    我們是不是有順利拿到登入 token。
    """
    assert auth_session["token"], "登入後應該拿到 access token"


@pytest.mark.api
@pytest.mark.regression
def test_authenticated_user_profile_matches_login_user(api_client, auth_session, settings):
    """
    先登入，再去拿目前使用者資料。

    如果回來的 username 跟登入帳號一樣，
    代表登入流程和授權流程有順利接起來。
    """
    response = api_client.get(
        "/auth/me",
        headers=api_client.authorized_headers(auth_session["token"]),
    )

    assert response.status_code == 200, "帶著有效 token 時，/auth/me 應該回 200"

    profile = response.json()

    # 這裡不是在硬猜資料，而是在比對「登入時用的帳號」和「API 說你是誰」是不是同一個人。
    assert profile["username"] == settings["username"], "目前登入的使用者應該和測試帳號一致"
