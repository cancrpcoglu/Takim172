import streamlit as st
from services.api import api_request
import time

st.title("🔐 Giriş Yap")

# Form alanları
email = st.text_input("E-posta")
password = st.text_input("Şifre", type="password")

if st.button("Giriş"):
    if email and password:
        # 1. Login isteği
        res = api_request(
            "POST", 
            "/users/login", 
            {"email": email, "password": password}
        )

        if res and "access_token" in res:
            # 2. Token'ı kaydet
            st.session_state.token = res["access_token"]

            # 3. Rolü DOĞRUDAN res içinden al (Backend'de eklediğimiz kısım)
            # Eğer backend'de return {"user": {"role": ...}} yaptıysan:
            user_info = res.get("user", {}) 
            
            # Backend'den gelen rolü al, gelmezse 'hata' yaz ki 'user' ile karışmasın
            current_role = user_info.get("role", "role_bulunamadi") 
            
            st.session_state.role = current_role
            st.session_state.user_id = user_info.get("id")

            # Debug için ekranda gör (Hata çözülünce silebilirsin)
            # st.write(f"Sistemdeki Rolünüz: {st.session_state.role}")

            if current_role == "role_bulunamadi":
                st.error("Backend'den rol bilgisi gelmedi. Lütfen backend login return kısmını kontrol edin.")
            else:
                st.success(f"Giriş başarılı! Hoş geldin {current_role}")
                time.sleep(1)

                # 4. Yönlendirme
                if current_role == "admin":
                    st.switch_page("pages/admin.py")
                elif current_role == "seller":
                    st.switch_page("pages/seller.py")
                else:
                    st.switch_page("pages/user.py")
        else:
            st.error(res.get("detail", "Login başarısız"))