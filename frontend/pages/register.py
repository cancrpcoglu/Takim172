import streamlit as st
from services.api import api_request
import time

st.set_page_config(
    page_title="Kayıt Ol",
    page_icon="📝",
    layout="centered"
)

# Oturum kontrolü - zaten giriş yaptıysa direkt panele yönlendir
if st.session_state.get("token"):
    if st.session_state.get("role") == "user":
        st.switch_page("pages/user.py")
    elif st.session_state.get("role") == "seller":
        st.switch_page("pages/seller.py")
    else:
        st.switch_page("login.py")

st.title("📝 Hesap Oluştur")
st.markdown("Aramıza katılın!")

with st.form("register_form"):
    email = st.text_input("E-posta", placeholder="ornek@email.com")
    password = st.text_input("Şifre", type="password", placeholder="********")
    confirm_password = st.text_input("Şifre Tekrar", type="password", placeholder="********")
    
    submitted = st.form_submit_button("Kayıt Ol", type="primary", use_container_width=True)
    
    if submitted:
        # Validasyon
        if not email or "@" not in email:
            st.error("❌ Geçerli bir e-posta adresi girin")
        elif not password:
            st.error("❌ Şifre gerekli")
        elif len(password) < 6:
            st.error("❌ Şifre en az 6 karakter olmalı")
        elif password != confirm_password:
            st.error("❌ Şifreler eşleşmiyor")
        else:
            # 1. Kayıt ol (role default "user" olarak gönder)
            register_data = {
                "email": email,
                "password": password,
                "role": "user"  # Varsayılan olarak müşteri
            }
            
            response = api_request("POST", "/users/register", register_data)
            
            if response and response.get("success"):
                st.success("✅ Hesabınız oluşturuldu!")
                
                # 2. Otomatik giriş yap
                with st.spinner("Giriş yapılıyor..."):
                    login_data = {
                        "email": email,
                        "password": password
                    }
                    
                    login_response = api_request("POST", "/users/login", login_data)
                    
                    if login_response and login_response.get("access_token"):
                        # Token ve kullanıcı bilgilerini session'a kaydet
                        st.session_state["token"] = login_response.get("access_token")
                        st.session_state["authenticated"] = True
                        st.session_state["role"] = "user"  # Varsayılan rol
                        st.session_state["username"] = email.split("@")[0]
                        st.session_state["email"] = email
                        
                        st.success("🔐 Otomatik giriş yapıldı!")
                        st.balloons()
                        
                        time.sleep(1)
                        
                        # Müşteri paneline yönlendir
                        st.switch_page("pages/user.py")
                    else:
                        st.error("❌ Otomatik giriş başarısız, lütfen manuel giriş yapın")
                        time.sleep(1)
                        st.switch_page("login.py")
            elif response and response.get("detail"):
                st.error(f"❌ {response.get('detail')}")
            else:
                st.error("❌ Kayıt sırasında bir hata oluştu")
                st.write(response)

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔐 Zaten hesabın var mı? Giriş yap", use_container_width=True):
        st.switch_page("login.py")