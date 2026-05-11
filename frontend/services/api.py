import streamlit as st
import requests
import json

def api_request(method, endpoint, data=None):
    BASE_URL = "http://localhost:8000"
    url = f"{BASE_URL}{endpoint}"
    
    token = st.session_state.get("token")
    
    params = {}
    if token:
        params["token"] = token
    
    try:
        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=data, params=params)
        elif method == "PUT":
            response = requests.put(url, json=data, params=params)
        elif method == "DELETE":
            response = requests.delete(url, params=params)
        else:
            return {"error": f"Metod {method} desteklenmiyor"}
        
        # 200-299 arası tüm başarılı kodları kabul et
        if 200 <= response.status_code < 300:
            return response.json() if response.text else {}
        else:
            return {
                "error": f"HTTP {response.status_code}",
                "detail": response.text
            }
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "detail": response.text}
    except Exception as e:
        return {"error": str(e)}