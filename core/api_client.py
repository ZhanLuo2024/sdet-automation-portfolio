from __future__ import annotations

from typing import Any

from requests import Response, Session


class APIClient:
    """
    封裝所有 HTTP 請求邏輯的共用客戶端。

    測試不應該直接散落 requests.get() / requests.post()，
    原因是一旦 base URL、timeout、headers 規則需要調整，
    就必須找出每一個分散的呼叫點逐一修改，維護成本很高。

    透過 APIClient 集中管理，這些細節只需要在一個地方改。
    """

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        # rstrip("/") 去除尾部多餘的斜線，
        # 避免和 path 拼接時出現 double slash（例如 https://example.com//users）。
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # 使用 Session 而非單次 requests.get()，
        # 好處是 Session 會自動保留 cookies，並對同一 host 重用 TCP 連線，效能較好。
        self.session = Session()

    def _build_url(self, path: str) -> str:
        # lstrip("/") 去除 path 開頭多餘的斜線，確保拼接結果乾淨。
        # 例如 path="/users" 和 path="users" 都能正確產生 https://example.com/users。
        clean_path = path.lstrip("/")
        return f"{self.base_url}/{clean_path}"

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Response:
        """
        所有 HTTP 請求的統一入口。

        get() 和 post() 都是這個方法的語法糖，
        實際發送請求的邏輯只存在於這一個地方。
        這樣做的好處是：未來要加 retry 邏輯、統一 logging、或攔截請求，
        只需要修改這裡，不用動 get() / post() 等上層方法。
        """
        return self.session.request(
            method=method,
            url=self._build_url(path),
            headers=headers,
            json=json,
            timeout=self.timeout,
        )

    def get(self, path: str, *, headers: dict[str, str] | None = None) -> Response:
        """發送 GET 請求的便捷方法。"""
        return self.request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Response:
        """發送 POST 請求的便捷方法。"""
        return self.request("POST", path, headers=headers, json=json)

    def login(self, username: str, password: str) -> Response:
        """
        封裝登入請求。

        把登入邏輯獨立成一個方法，而不是讓每個測試自己組裝 payload，
        這樣當登入 API 的規格改變時（例如新增 MFA 欄位），
        只需要修改這一個方法，所有依賴它的測試自動跟著更新。
        """
        return self.post(
            "/auth/login",
            json={
                "username": username,
                "password": password,
            },
        )

    def authorized_headers(self, token: str) -> dict[str, str]:
        """
        產生帶有 Bearer token 的 Authorization header。

        集中產生 header 字串，避免各個測試自己拼接，
        減少因為拼字錯誤（例如少了空格）而導致的授權失敗。
        """
        return {"Authorization": f"Bearer {token}"}
