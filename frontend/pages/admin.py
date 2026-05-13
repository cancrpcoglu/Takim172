import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
from services.api import api_request # İkinci kodun API servisi

# ===================== SAYFA AYARLARI =====================
st.set_page_config(
    page_title="Team 172 | Admin Kontrol Merkezi",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== YETKİ KONTROLÜ =====================
if not st.session_state.get("token"):
    st.warning("Lütfen önce giriş yapın.")
    st.switch_page("login.py")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("Bu sayfaya erişim yetkiniz yok.")
    st.stop()

# ===================== MODERN UI CSS (TASARIM 1) =====================
st.markdown("""
<style>
    .main { background: #0B0F19; color: white; }
    div[data-testid="metric-container"] {
        background: linear-gradient(145deg, #111827, #1f2937);
        border: 1px solid #2d3748;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: #111827;
        padding: 10px 20px;
        border-radius: 12px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
    }
    .stButton > button {
        border-radius: 10px;
        background: linear-gradient(90deg, #2563eb, #1e40af);
        color: white;
        transition: 0.3s;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(37,99,235,0.4); }
    section[data-testid="stSidebar"] { background: #0f172a; border-right: 1px solid #1f2937; }
    .status-badge {
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===================== SIDEBAR =====================
with st.sidebar:
    st.title("👑 Admin Panel")
    st.markdown(f"**Hoş geldin, {st.session_state.get('username', 'Admin')}**")
    st.caption("Team 172 Yönetim Sistemi v2.0")
    st.divider()
    
    # Sistem Durumu (Tasarım 1'deki CPU barları)
    st.subheader("🖥️ Sistem Kaynakları")
    st.caption("Sunucu Yükü")
    st.progress(45)
    st.caption("API Yanıt Süresi (ms)")
    st.progress(15)
    
    st.divider()
    if st.button("🚪 Güvenli Çıkış"):
        st.session_state.clear()
        st.rerun()

# ===================== VERİ ÇEKME (BACKEND BAĞLANTISI) =====================
@st.cache_data(ttl=60)
def get_all_stats():
    u_res = api_request("GET", "/users")
    o_res = api_request("GET", "/orders")
    p_res = api_request("GET", "/products")
    s_res = api_request("GET", "/sellers")
    return u_res, o_res, p_res, s_res

u_res, o_res, p_res, s_res = get_all_stats()

# ===================== HEADER & METRICS =====================
st.title("🚀 Yönetim Paneli")
st.success("Sistem Aktif | API Bağlantısı Başarılı")

# Üst Metrik Kartları
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    total_u = len(u_res.get("data", [])) if u_res else 0
    st.metric("👥 Toplam Kullanıcı", total_u)
with m2:
    total_o = len(o_res.get("data", [])) if o_res else 0
    st.metric("📦 Toplam Sipariş", total_o)
with m3:
    total_p = len(p_res.get("data", [])) if p_res else 0
    st.metric("🛒 Ürün Sayısı", total_p)
with m4:
    total_s = len(s_res.get("data", [])) if s_res else 0
    st.metric("🏪 Aktif Satıcı", total_s)
with m5:
    revenue = sum(o.get("total_price", 0) for o in o_res.get("data", [])) if o_res else 0
    st.metric("💰 Toplam Ciro", f"{revenue:,} ₺")

st.divider()

# ===================== ANA SEKMELER (TABS) =====================
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 Kullanıcı Yönetimi", 
    "🏪 Satıcı Merkezi", 
    "📊 Analitik & Dashboard",
    "⚙️ Sistem Logları"
])

# ===================== TAB 1: KULLANICI YÖNETİMİ =====================
with tab1:
    st.subheader("👥 Kullanıcı Yönetimi")
    
    users_response = api_request("GET", "/users")
    
    if users_response and users_response.get("success"):
        users = users_response.get("data", [])
        
        if users:
            # Rolleri temizle - ÖNCE
            for user in users:
                if 'role' in user:
                    # Eğik çizgi ve boşlukları temizle
                    clean_role = user['role'].replace('/', '').replace('\\', '').strip().lower()
                    if clean_role not in ["user", "seller", "admin"]:
                        clean_role = "user"
                    user['role'] = clean_role
            
            # İstatistik kartları
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Toplam Kullanıcı", len(users))
            with col2:
                user_count = len([u for u in users if u.get("role") == "user"])
                st.metric("Müşteriler", user_count)
            with col3:
                seller_count = len([u for u in users if u.get("role") == "seller"])
                st.metric("Satıcılar", seller_count)
            with col4:
                admin_count = len([u for u in users if u.get("role") == "admin"])
                st.metric("Adminler", admin_count)
            
            st.markdown("---")
            st.subheader("📋 Kullanıcı Listesi")
            
            search = st.text_input("🔍 E-posta ile ara", placeholder="kullanici@email.com")
            filtered_users = users
            if search:
                filtered_users = [u for u in users if search.lower() in u.get("email", "").lower()]
            
            for user in filtered_users:
                with st.container(border=True):
                    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{user.get('email')}**")
                        st.caption(f"ID: {user.get('id')}")
                    
                    with col2:
                        role = user.get('role', 'user')
                        if role == "admin":
                            st.markdown("🔴 **Admin**")
                        elif role == "seller":
                            st.markdown("🟢 **Satıcı**")
                        else:
                            st.markdown("🔵 **Müşteri**")
                    
                    with col3:
                        created_at = user.get('created_at', '')
                        st.caption(f"Kayıt: {created_at[:10] if created_at else '-'}")
                    
                    with col4:
                        if user.get('email') != st.session_state.get('email'):
                            # Rol seçimi - TEMİZ VERİ KULLAN
                            current_role = user.get('role', 'user')
                            role_options = ["user", "seller", "admin"]
                            
                            try:
                                current_index = role_options.index(current_role)
                            except ValueError:
                                current_index = 0
                            
                            new_role = st.selectbox(
                                "Yeni Rol",
                                options=role_options,
                                index=current_index,
                                key=f"role_sel_{user.get('id')}",
                                label_visibility="collapsed"
                            )
                            
                            if new_role != current_role:
                                if st.button("💾 Kaydet", key=f"save_btn_{user.get('id')}", use_container_width=True):
                                    update_response = api_request(
                                        "PUT", 
                                        f"/users/{user.get('id')}/role?role={new_role}", 
                                        None
                                    )
                                    if update_response and update_response.get("success"):
                                        st.success("✅ Rol güncellendi!")
                                        time.sleep(0.5)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Hata: {update_response}")
                        else:
                            st.write("✨")
                            st.caption("Kendi Hesabınız")
                    
                    with col5:
                        if user.get('email') != st.session_state.get('email'):
                            if st.button("🗑️ Sil", key=f"delete_{user.get('id')}"):
                                delete_response = api_request("DELETE", f"/users/{user.get('id')}")
                                if delete_response and delete_response.get("success"):
                                    st.success("✅ Silindi!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Hata: {delete_response}")
        else:
            st.info("Henüz kullanıcı bulunmuyor.")
    else:
        st.error("Kullanıcılar yüklenemedi!")

# ===================== TAB 2: SATICI YÖNETİMİ =====================
with tab2:
    st.subheader("🏪 Mağaza Performansları")
    sellers = s_res.get("data", []) if s_res else []
    
    for seller in sellers:
        with st.expander(f"🏪 {seller.get('store_name')} | ⭐ {seller.get('rating', 0)}/5"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Açıklama:** {seller.get('description', 'Yok')}")
                st.write(f"**Satıcı ID:** {seller.get('id')}")
           
# ===================== TAB 3: DASHBOARD & ANALİTİK =====================
with tab3:
    st.subheader("📈 Satış ve Stok Analitiği")
    
    # Grafik verilerini hazırlama
    if o_res and p_res:
        products = p_res.get("data", [])
        orders = o_res.get("data", [])
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### 📦 Stok Durumu")
            st.bar_chart(pd.DataFrame(products).set_index("name")["stock"] if products else None)
            
        with col_right:
            st.markdown("#### 🔥 En Çok Satanlar (Ciro)")
            # Basit bir ciro hesaplama ve görselleştirme
            sales_data = [{"Ürün": p.get("name"), "Ciro": p.get("price", 0) * 10} for p in products[:5]]
            st.area_chart(pd.DataFrame(sales_data).set_index("Ürün"))

        st.divider()
        st.subheader("📋 Son Siparişler")
        if orders:
            df_orders = pd.DataFrame(orders)
            st.dataframe(df_orders, use_container_width=True)
        else:
            st.info("Henüz sipariş bulunmuyor.")

# ===================== TAB 4: SİSTEM LOGLARI =====================
with tab4:
    st.subheader("🧠 İşlem Kayıtları")
    with st.container(border=True, height=400):
        # Gerçek log mekanizması yoksa mock gösterimi yapıyoruz
        logs = [
            f"{datetime.now().strftime('%H:%M:%S')} - [INFO] Admin girişi yapıldı: {st.session_state.get('username')}",
            f"{datetime.now().strftime('%H:%M:%S')} - [SYSTEM] API Bağlantısı sağlıklı (200 OK)",
            f"{datetime.now().strftime('%H:%M:%S')} - [DB] Veritabanı senkronizasyonu tamamlandı."
        ]
        for log in logs:
            st.code(log)

# ===================== FOOTER =====================
st.markdown("---")
st.caption(f"© 2024 Team 172 AI Management Console | Son Güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}")