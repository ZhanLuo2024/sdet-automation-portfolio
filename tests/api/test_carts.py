import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_carts_endpoint_is_available(api_client):
    """
    先做一個最小檢查：
    看購物車清單 API 有沒有正常工作。
    """
    response = api_client.get("/carts")

    assert response.status_code == 200, "購物車清單 API 應該可正常存取"

    payload = response.json()
    assert "carts" in payload, "回傳資料裡應該要有 carts 清單"
    assert isinstance(payload["carts"], list), "carts 應該是一個列表"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(
    "cart_id, expected_total_products",
    [
        # 這兩組數字來自 DummyJSON 文件目前提供的範例資料。
        # 我們把它寫在這裡，是要確認「固定範例資料」的內容沒有意外改變。
        # 如果未來官方資料更新，這裡也應該跟著一起調整。
        (1, 4),
        (2, 5),
    ],
)
def test_cart_details_match_expected_examples(api_client, cart_id, expected_total_products):
    """
    用參數化一次檢查多個 cart。

    Pytest 會幫我們把這個測試拆成多次獨立執行，
    所以哪一組失敗，一眼就能看出來。
    """
    response = api_client.get(f"/carts/{cart_id}")

    assert response.status_code == 200, f"cart {cart_id} 應該存在"

    cart = response.json()

    # 這裡確認 API 真的回了我們要的那台購物車。
    assert cart["id"] == cart_id, "回傳的 cart id 應該和查詢的 id 一樣"
    assert cart["totalProducts"] == expected_total_products, "範例 cart 的商品數量應該符合預期"
