import streamlit as st

st.set_page_config(page_title="Kobi AI Panel", layout="wide")

st.title("🚀 Kobi AI E-Ticaret Yönetim Sistemi")
st.write("Sol taraftaki menüden giriş yapabilir veya kayıt olabilirsiniz.")

if "token" in st.session_state:
    st.success(f"Hoş geldin! Rolün: {st.session_state.get('role')}")
else:
    st.info("Lütfen devam etmek için Login sayfasından giriş yapın.")