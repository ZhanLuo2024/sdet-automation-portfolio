import requests

def test_api_is_working(base_url):
    """測試 API 伺服器有沒有活著 (狀態碼 200)"""
    response = requests.get(f"{base_url}/products")
    assert response.status_code == 200, f"伺服器錯誤！狀態碼: {response.status_code}"

def test_product_data_structure(base_url):
    """驗證拿到的商品一定會有 id 欄位"""
    response = requests.get(f"{base_url}/products/1")
    data = response.json()
    
    # 驗證 'id' 這個 key 存在於我們拿回來的 json 資料中
    assert "id" in data, "商品資料結構錯了，缺少 id 欄位！"
