import streamlit as st
from services.api import api_request
import time
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Satıcı Paneli",
    page_icon="🏪",
    layout="wide"
)

# Yetki kontrolü
if not st.session_state.get("token"):
    st.warning("Lütfen önce giriş yapın.")
    st.switch_page("login.py")

if st.session_state.get("role") != "seller":
    st.error("Bu sayfaya erişim yetkiniz yok. Bu sayfa sadece satıcılar içindir.")
    st.stop()

# Seller ID'yi al veya kaydet
def get_seller_id():
    """Satıcının ID'sini al"""
    if "seller_id" in st.session_state:
        return st.session_state.seller_id
    
    seller_info = api_request("GET", "/sellers/me")
    if seller_info and seller_info.get("success"):
        seller_data = seller_info.get("data")
        seller_id = seller_data.get("id")
        st.session_state.seller_id = seller_id
        st.session_state.store_name = seller_data.get("store_name")
        return seller_id
    return None

# Sidebar - Satıcı Bilgileri
st.sidebar.title(f"🏪 Hoş geldin, {st.session_state.get('username', 'Satıcı')}")

# Mağaza bilgisini kontrol et
seller_info = api_request("GET", "/sellers/me")
seller_data = None

if seller_info and seller_info.get("success"):
    seller_data = seller_info.get("data")
    st.session_state.seller_id = seller_data.get("id")
    st.session_state.store_name = seller_data.get("store_name")
    st.sidebar.success(f"✅ Mağaza: {seller_data.get('store_name', 'Belirsiz')}")
    st.sidebar.markdown(f"**⭐ Rating:** {seller_data.get('rating', 0)}/5")
else:
    st.sidebar.warning("⚠️ Henüz mağaza kaydınız yok!")
    with st.sidebar:
        with st.form("register_store"):
            st.subheader("🏪 Mağaza Kaydı")
            store_name = st.text_input("Mağaza Adı")
            description = st.text_area("Mağaza Açıklaması")
            
            if st.form_submit_button("Mağaza Oluştur", type="primary"):
                if store_name and description:
                    response = api_request("POST", "/sellers/register", {
                        "store_name": store_name,
                        "description": description,
                        "rating": 0
                    })
                    if response and response.get("success"):
                        st.success("✅ Mağaza oluşturuldu!")
                        st.rerun()
                    else:
                        st.error(f"❌ Hata: {response.get('detail', 'Bilinmeyen hata')}")
                else:
                    st.error("Tüm alanları doldurun")

st.sidebar.markdown("---")

# Ana sekmeler
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "🛍️ Ürünlerim", 
    "📦 Siparişler", 
    "🚚 Kargo Yönetimi",
    "🤖 AI Asistan"
])

# ==================== TAB 1: DASHBOARD ====================
with tab1:
    st.subheader("📊 Satış Dashboard'u")
    
    seller_id = get_seller_id()
    
    # Siparişleri getir - DOĞRU ENDPOINT
    orders_response = api_request("GET", "/orders/my")  # /my değil, /orders/my
    
    all_orders = []
    if orders_response:
        if isinstance(orders_response, dict):
            if orders_response.get("success"):
                all_orders = orders_response.get("data", [])
            elif orders_response.get("data"):
                all_orders = orders_response.get("data", [])
        elif isinstance(orders_response, list):
            all_orders = orders_response
    
   
    
    # Ürünleri getir
    products_response = api_request("GET", "/products")
    all_products = []
    if products_response:
        if isinstance(products_response, dict):
            if products_response.get("success"):
                all_products = products_response.get("data", [])
            elif products_response.get("data"):
                all_products = products_response.get("data", [])
        elif isinstance(products_response, list):
            all_products = products_response
    
    # Satıcının ürünlerini filtrele
    my_products = []
    my_orders = []
    
    if seller_id:
        my_products = [p for p in all_products if p.get("seller_id") == seller_id]
        my_product_ids = [p.get("id") for p in my_products]
        my_orders = [o for o in all_orders if o.get("product_id") in my_product_ids]
        
       
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📦 Toplam Ürün", len(my_products))
    with col2:
        st.metric("📋 Toplam Sipariş", len(my_orders))
    with col3:
        total_revenue = sum(o.get("total_amount", 0) or 0 for o in my_orders)
        st.metric("💰 Toplam Gelir", f"{total_revenue:,.2f} TL")
    with col4:
        rating = seller_data.get('rating', 0) if seller_data else 0
        st.metric("⭐ Mağaza Puanı", f"{rating}/5")

    st.markdown("---")
    
    if my_orders:
        st.subheader("📈 Son Siparişler")
        try:
            orders_df = pd.DataFrame(my_orders)
            if 'created_at' in orders_df.columns:
                orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])
                orders_df = orders_df.sort_values('created_at', ascending=False)
            
            show_cols = [c for c in ['id', 'product_id', 'quantity', 'status', 'created_at'] if c in orders_df.columns]
            st.dataframe(orders_df[show_cols].head(10), use_container_width=True)
            
            # Durum dağılımı
            if 'status' in orders_df.columns:
                st.subheader("📊 Durum Dağılımı")
                status_counts = orders_df['status'].value_counts()
                st.bar_chart(status_counts)
        except Exception as e:
            st.error(f"Veri gösterilirken hata: {e}")
    else:
        st.info("📭 Henüz siparişiniz bulunmuyor.")

# ==================== TAB 2: ÜRÜN YÖNETİMİ ====================
with tab2:
    st.subheader("🛍️ Ürün Yönetimi")
    
    # Yeni ürün ekleme
    with st.expander("➕ Yeni Ürün Ekle", expanded=False):
        with st.form("add_product"):
            col1, col2 = st.columns(2)
            with col1:
                p_name = st.text_input("Ürün Adı *")
                p_price = st.number_input("Fiyat (TL) *", min_value=0.01, step=1.0)
            with col2:
                p_stock = st.number_input("Stok Miktarı *", min_value=0, step=1)
                p_desc = st.text_area("Ürün Açıklaması")
            
            if st.form_submit_button("Ürün Ekle", type="primary"):
                s_id = get_seller_id()
                if s_id and p_name and p_price > 0:
                    res = api_request("POST", "/products", {
                        "name": p_name, 
                        "description": p_desc, 
                        "price": p_price, 
                        "stock": p_stock, 
                        "seller_id": s_id
                    })
                    if res and res.get("success"):
                        st.success("✅ Ürün eklendi!")
                        st.rerun()
                    else:
                        error_msg = res.get('detail', 'Bilinmeyen hata') if res else 'Bağlantı hatası'
                        st.error(f"❌ Ürün eklenemedi: {error_msg}")
                else:
                    st.error("❌ Ürün adı ve fiyat zorunludur!")

    st.markdown("---")
    st.subheader("📋 Mevcut Ürünlerim")
    
    # Ürünleri listele
    p_res = api_request("GET", "/products")
    seller_id = get_seller_id()
    
    if p_res and seller_id:
        # Veriyi normalize et
        if isinstance(p_res, dict):
            all_products = p_res.get("data", []) if p_res.get("success") else p_res.get("data", [])
        else:
            all_products = p_res if isinstance(p_res, list) else []
        
        my_products = [p for p in all_products if p.get("seller_id") == seller_id]
        
        if my_products:
            for p in my_products:
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.markdown(f"**{p.get('name')}**")
                        st.caption(p.get('description', 'Açıklama yok')[:80])
                    with col2:
                        st.metric("Fiyat", f"{p.get('price', 0)} TL")
                        st.metric("Stok", p.get('stock', 0))
                    with col3:
                        if st.button("✏️ Düzenle", key=f"edit_{p.get('id')}"):
                            st.session_state.editing_product = p
                            st.rerun()
                    with col4:
                        if st.button("🗑️ Sil", key=f"del_{p.get('id')}"):
                            del_res = api_request("DELETE", f"/products/{p.get('id')}")
                            if del_res and del_res.get("success"):
                                st.success("Ürün silindi!")
                                st.rerun()
                            else:
                                st.error("Silme başarısız!")
            
            # Düzenleme formu
            if st.session_state.get("editing_product"):
                p = st.session_state.editing_product
                with st.expander(f"✏️ Ürün Düzenle: {p.get('name')}", expanded=True):
                    with st.form("edit_product"):
                        edit_name = st.text_input("Ürün Adı", value=p.get('name'))
                        edit_price = st.number_input("Fiyat", value=float(p.get('price', 0)), step=1.0)
                        edit_stock = st.number_input("Stok", value=int(p.get('stock', 0)), step=1)
                        edit_desc = st.text_area("Açıklama", value=p.get('description', ''))
                        
                        if st.form_submit_button("Güncelle"):
                            update_data = {
                                "name": edit_name,
                                "price": edit_price,
                                "stock": edit_stock,
                                "description": edit_desc
                            }
                            update_res = api_request("PUT", f"/products/{p.get('id')}", update_data)
                            if update_res and update_res.get("success"):
                                st.success("Ürün güncellendi!")
                                del st.session_state.editing_product
                                st.rerun()
                            else:
                                st.error("Güncelleme başarısız!")
                        
                        if st.button("İptal"):
                            del st.session_state.editing_product
                            st.rerun()
        else:
            st.info("📭 Henüz ürün eklememişsiniz.")
    else:
        st.info("Ürünler yüklenemedi.")

# ==================== TAB 3: SİPARİŞLER  ====================

with tab3:
    st.subheader("📦 Gelen Siparişler")
    
    # API'den sadece bu satıcıya/kullanıcıya ait siparişleri çekiyoruz
    response = api_request("GET", "/orders/my")
    
    if response and response.get("success"):
        orders_data = response.get("data", [])
        
        if not orders_data:
            st.info("📭 Henüz bir sipariş kaydı bulunmuyor.")
        else:
            # 1. Özet Tablo Görünümü
            df = pd.DataFrame(orders_data)
            
            # Tabloda sadece önemli kolonları gösterelim
            view_cols = ["id", "product_id", "quantity", "status", "created_at"]
            # Var olan kolonları filtrele (hata almamak için)
            existing_cols = [c for c in view_cols if c in df.columns]
            
            st.dataframe(df[existing_cols], use_container_width=True)
            
            st.markdown("---")
            
            # 2. Detaylı Kart Görünümü ve İşlemler
            st.subheader("📋 Sipariş Detayları ve Yönetim")
            for order in orders_data:
                # Duruma göre renkli badge/etiket mantığı
                status = order.get('status', 'pending')
                status_emoji = "⏳" if status == "pending" else "✅" if status == "shipped" else "❌"
                
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**Sipariş #{order.get('id')}**")
                        st.caption(f"Tarih: {order.get('created_at', '')[:10]}")
                    
                    with col2:
                        st.write(f"**Adet:** {order.get('quantity')}")
                        st.write(f"**Durum:** {status_emoji} {status.upper()}")
                        
                    with col3:
                        # Eğer kargo tabına yönlendirmek istersen veya işlem yapmak istersen
                        if status == 'pending':
                            if st.button("Kargola 🚚", key=f"ship_btn_{order.get('id')}"):
                                # Kargo tabına yönlendirme veya modal açma mantığı
                                st.session_state.shipment_order = order
                                st.success("Kargo Yönetimi sekmesine giderek işlemi tamamlayabilirsiniz.")
    else:
        st.error("⚠️ Sipariş verileri alınamadı. Lütfen bağlantınızı kontrol edin.")
# ==================== TAB 4: KARGO YÖNETİMİ ====================
with tab4:
    st.subheader("🚚 Kargo Yönetimi")
    
    seller_id = get_seller_id()
    
    # Siparişleri getir
    orders_response = api_request("GET", "/orders")
    all_orders = []
    if orders_response:
        if isinstance(orders_response, dict):
            if orders_response.get("success"):
                all_orders = orders_response.get("data", [])
            elif orders_response.get("data"):
                all_orders = orders_response.get("data", [])
        elif isinstance(orders_response, list):
            all_orders = orders_response
    
    # Ürünleri getir
    products_response = api_request("GET", "/products")
    all_products = []
    if products_response:
        if isinstance(products_response, dict):
            if products_response.get("success"):
                all_products = products_response.get("data", [])
            elif products_response.get("data"):
                all_products = products_response.get("data", [])
        elif isinstance(products_response, list):
            all_products = products_response
    
    if seller_id:
        my_product_ids = [p.get("id") for p in all_products if p.get("seller_id") == seller_id]
        my_orders = [o for o in all_orders if o.get("product_id") in my_product_ids]
        pending_orders = [o for o in my_orders if o.get('status') == 'pending']
        
        if pending_orders:
            st.subheader("📦 Kargo Bekleyen Siparişler")
            
            for order in pending_orders:
                product = next((p for p in all_products if p.get("id") == order.get("product_id")), {})
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        st.write(f"Sipariş #{order.get('id')}")
                        st.write(f"Ürün: {product.get('name', 'Bilinmiyor')}")
                    with col2:
                        st.write(f"Adet: {order.get('quantity')}")
                        st.write(f"Müşteri ID: {order.get('user_id')}")
                    with col3:
                        if st.button("🚚 Kargo Oluştur", key=f"ship_{order.get('id')}"):
                            st.session_state.shipment_order = order
                            st.rerun()
        else:
            st.info("📭")
        
        # Kargo oluşturma formu
        if st.session_state.get("shipment_order"):
            order = st.session_state.shipment_order
            with st.form("ship_form"):
                st.subheader(f"Sipariş #{order.get('id')} için Kargo")
                company = st.selectbox("Kargo Şirketi", ["Aras Kargo", "Yurtiçi Kargo", "MNG Kargo", "PTT Kargo", "Sürat Kargo"])
                tracking = st.text_input("Takip Numarası", placeholder="örn: 1234567890")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("✅ Kargoyu Oluştur"):
                        res = api_request("POST", "/shipments", {
                            "order_id": order.get('id'), 
                            "cargo_company": company, 
                            "tracking_number": tracking
                        })
                        if res and res.get("success"):
                            # Sipariş durumunu güncelle
                            api_request("PUT", f"/orders/{id}/status", data={"status": "shipped"})
                            st.success("✅ Kargo oluşturuldu ve sipariş kargolandı!")
                            del st.session_state.shipment_order
                            st.rerun()
                        else:
                            error_msg = res.get('detail', 'Bilinmeyen hata') if res else 'Bağlantı hatası'
                            st.error(f"❌ Kargo oluşturulamadı: {error_msg}")
                with col2:
                    if st.form_submit_button("❌ İptal"):
                        del st.session_state.shipment_order
                        st.rerun()
        
       
# ==================== TAB 5: AI ASİSTAN ====================
with tab5:
    st.subheader("🤖 AI Satıcı Asistanı")
    st.caption("💡 Sorabileceğiniz örnek sorular: Bu ay satışlar nasıl? | Hangi ürünler az satıyor? | Geciken kargolar var mı?")
    
    if "seller_ai_messages" not in st.session_state:
        st.session_state.seller_ai_messages = []
    
    for msg in st.session_state.seller_ai_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Sorunuzu yazın..."):
        st.session_state.seller_ai_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        response = api_request("POST", "/ai/seller-chat", {"message": prompt})
        
        if response:
            if isinstance(response, dict):
                answer = response.get("message") or response.get("response") or response.get("data") or str(response)
            else:
                answer = str(response)
        else:
            answer = "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
        
        st.session_state.seller_ai_messages.append({"role": "assistant", "content": answer})
        st.rerun()