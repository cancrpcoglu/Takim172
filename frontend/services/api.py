import streamlit as st
import requests
import json

def api_request(method, endpoint, data=None):
    # 1. Base URL'i tanımla
    BASE_URL = "http://localhost:8000"
    
    # 2. Endpoint'in başında '/' olduğundan ve sonunda '/' OLDUĞUNDAN emin ol
    # Bu, 307 Redirect ve 404 hatalarını önler.
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    if not endpoint.endswith("/"):
        endpoint = endpoint + "/"
        
    url = f"{BASE_URL}{endpoint}"
    
    # 3. Token'ı al
    token = st.session_state.get("token")
    
    # 4. FastAPI genellikle token'ı Header içinde 'Authorization: Bearer <token>' olarak bekler.
    # Loglarında query param (params) olarak gördüm, o yüzden params'ı da tutuyoruz.
    params = {}
    headers = {}
    if token:
        params["token"] = token  # Mevcut yapını bozmamak için
   # Standart f-string kullanımı
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        # İsteği gönder (headers eklenmiş haliyle)
        if method == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, params=params, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, params=params, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, params=params, headers=headers)
        else:
            return {"success": False, "error": f"Metod {method} desteklenmiyor"}
        
        # Loglardaki 404/403 takibini kolaylaştırmak için konsola yazdırabilirsin
        # print(f"Request: {method} {url} - Status: {response.status_code}")

        if 200 <= response.status_code < 300:
            return response.json() if response.text else {"success": True}
        else:
            # Hata durumunda detaylı bilgi dön
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
                
            return {
                "success": False,
                "error": f"HTTP {response.status_code}",
                "detail": error_detail
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}