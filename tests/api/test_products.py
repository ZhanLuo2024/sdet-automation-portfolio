import pytest
import requests

class TestProductAPI:
  """
  測試商品相關的 API
  """

  def test_get_protected_resource(self, auth_token, base_url):
    """
    基礎測試： 利用拿到的 Auth Token 發送授權才可存取 API
    """

    # 組裝 Header（把 Token 塞進 Header）
    headers = {
      "Authorization": f"Bearer {auth_token}"
    }

    # 存取一個需要驗證的 Endpoint
    response = requests.get(f"{base_url}/auth/me", headers=headers)

    # 斷言伺服器確實接受了這個 token
    assert response.status_code == 200
    # 斷言回傳的使用者真的是我們剛剛登入的用戶
    assert response.json()["username"] == "emilys"


    # ------------------------------------------------------------- #
    # ⭐️ 必學重點：參數化測試 (Parametrization)
    # ------------------------------------------------------------- #
    # 在 iOS 裡，如果你要測試 3 個不同的商品 ID，你可能會寫一個 for-loop。
    # 在 Pytest 裡，我們絕對不推薦在腳本區塊裡寫 for-loop！
    # 取而代之的是使用 @pytest.mark.parametrize。
    
    # argnames: 你要傳給下面函數的參數名稱 (用逗號隔開的字串)
    # argvalues: 一個 List。裡面裝著多組的 Tuples 值。這裡提供了三組 (id, 預期類別)。
    @pytest.mark.parametrize("product_id, expected_category", [
      (1, "beauty"),
      (2, "beauty"),
      (121, "motorcycle")
    ])
    def test_verify_product_categories(self, product_id, expected_category, base_url):
      """
      利用參數化機制，這個 function 會被獨立、乾淨地執行「3次」！
      這三組測試的結果也是完全獨立的一綠兩紅，即使第一組失敗，第二三組依然會繼續跑。
      """
      response = requests.get(f"{base_url}/products/{product_id}")
      data = response.json()

      # 斷言成功
      assert response.status_code == 200

      # 斷言
      # 驗證該 API 返回特定商品的 Category 是否符合期待
      actual_category = data.get("category", "")

      assert actual_category == expected_category, f"ID {product_id} 的分類錯誤！預期是 {expected_category}, 拿到的是 {actual_category}"