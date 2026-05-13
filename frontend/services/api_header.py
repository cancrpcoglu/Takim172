# services/api_header.py - Authorization header version
import streamlit as st
import requests
import json

def api_request_header(method, endpoint, data=None):
    """Token'ı Authorization header olarak gönderir"""
    BASE_URL = "http://localhost:8000"
    url = f"{BASE_URL}{endpoint}"
    
    token = st.session_state.get("token")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return {"error": f"Metod {method} desteklenmiyor"}
        
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