import streamlit as st
from services.api import api_request
import time

st.set_page_config(page_title="Müşteri Paneli", layout="wide")

if st.session_state.get("role") != "user":
    st.warning("Bu sayfa sadece müşteriler içindir.")
    st.stop()

# Sepet için session state初始化
if "cart" not in st.session_state:
    st.session_state.cart = {}  # {product_id: {"product": product, "quantity": quantity}}

# Sidebar - Sepet Özeti
st.sidebar.title(f"👋 Hoş geldin, {st.session_state.get('username', 'Müşteri')}")

st.sidebar.markdown("---")
st.sidebar.subheader("🛒 Sepetim")

# Sepet özetini göster
cart_items = st.session_state.cart
total_items = sum(item["quantity"] for item in cart_items.values())
total_price = sum(item["product"].get("price", 0) * item["quantity"] for item in cart_items.values())

st.sidebar.markdown(f"**Ürün Sayısı:** {total_items}")
st.sidebar.markdown(f"**Toplam Tutar:** {total_price} TL")

if cart_items:
    if st.sidebar.button("📦 Sepeti Onayla", type="primary", use_container_width=True):
        with st.sidebar.status("Sipariş oluşturuluyor..."):
            success_count = 0
            fail_count = 0
            
            for product_id, item in cart_items.items():
                order_data = {
                    "product_id": product_id,
                    "quantity": item["quantity"]
                }
                result = api_request("POST", "/orders", order_data)
                
                if result and (result.get("success") == True or result.get("data")):
                    success_count += 1
                else:
                    fail_count += 1
                    st.error(f"{item['product'].get('name')} siparişi başarısız: {result}")
            
            if success_count > 0:
                st.success(f"✅ {success_count} ürün sipariş edildi!")
                st.session_state.cart = {}  # Sepeti temizle
                time.sleep(1)
                st.rerun()
            else:
                st.error("Hiçbir sipariş oluşturulamadı.")
    
    if st.sidebar.button("🗑️ Sepeti Temizle", use_container_width=True):
        st.session_state.cart = {}
        st.rerun()
else:
    st.sidebar.info("Sepetiniz boş")

# Ana sekme yapısı
tab1, tab2, tab3,tab4 = st.tabs(["🛍️ Ürünler", "📦 Siparişlerim", "🚚 Kargo Takibi","🤖 AI Asistan"])

# ==================== TAB 1: ÜRÜNLER (Sepete Ekle) ====================
with tab1:
    st.subheader("🛒 Ürünler")
    st.caption("Ürünleri sepete ekleyin, sonra sepetinizden onaylayın")
    
    # Ürünleri getir
    response = api_request("GET", "/products")
    
    if response and response.get("success"):
        products = response.get("data", [])
        
        if products:
            # Ürünleri grid şeklinde göster
            cols = st.columns(2)
            
            for idx, product in enumerate(products):
                with cols[idx % 2]:
                    with st.container(border=True):
                        st.markdown(f"**{product.get('name', 'Ürün')}**")
                        st.markdown(f"💰 **{product.get('price', 0)} TL**")
                        st.markdown(f"📦 Stok: {product.get('stock', 0)}")
                        
                        # Sepete ekleme formu
                        if product.get('stock', 0) > 0:
                            col_qty, col_btn = st.columns([2, 1])
                            with col_qty:
                                quantity = st.number_input(
                                    "Adet",
                                    min_value=1,
                                    max_value=product.get('stock', 10),
                                    value=1,
                                    key=f"cart_qty_{product.get('id')}",
                                    label_visibility="collapsed"
                                )
                            with col_btn:
                                if st.button("➕ Sepete Ekle", key=f"add_to_cart_{product.get('id')}"):
                                    # Sepete ekle
                                    if product.get('id') in st.session_state.cart:
                                        st.session_state.cart[product.get('id')]["quantity"] += quantity
                                    else:
                                        st.session_state.cart[product.get('id')] = {
                                            "product": product,
                                            "quantity": quantity
                                        }
                                    st.success(f"✅ {product.get('name')} sepete eklendi!")
                                    st.rerun()
                        else:
                            st.warning("Stokta yok")
        else:
            st.info("Henüz ürün bulunmuyor.")
    else:
        st.info("Ürünler yüklenemedi.")

# ==================== TAB 2: SİPARİŞLERİM ====================
with tab2:
    st.subheader("📋 Siparişlerim")
    
    orders_response = api_request("GET", "/orders/my")
    
    # Backend yanıtını işle
    if orders_response:
        if isinstance(orders_response, list):
            orders = orders_response
        elif isinstance(orders_response, dict) and orders_response.get("success"):
            orders = orders_response.get("data", [])
        elif isinstance(orders_response, dict) and orders_response.get("data"):
            orders = orders_response.get("data", [])
        else:
            orders = []
    else:
        orders = []
    
    if not orders:
        st.info("📭 Henüz hiç siparişiniz bulunmuyor.")
        st.info("💡 İpucu: Ürünler sekmesinden ürünleri sepete ekleyin ve sepeti onaylayın!")
    else:
        for order in orders:
            with st.expander(f"Sipariş #{order.get('id')} - {order.get('status', 'Beklemede').upper()}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Sipariş No", order.get('id', '-'))
                col2.metric("Durum", order.get('status', '-').capitalize())
                col3.metric("Tarih", order.get('created_at', '-')[:10] if order.get('created_at') else '-')
                
                st.metric("Ürün Adedi", order.get('quantity', '-'))
                st.metric("Ürün ID", order.get('product_id', '-'))
                
                # Toplam tutarı göster (eğer varsa)
                if order.get('total_amount'):
                    st.metric("Toplam Tutar", f"{order.get('total_amount')} TL")
                
                # İptal butonu
                if order.get('status') in ['pending', 'confirmed', 'processing']:
                    if st.button(f"❌ İptal Et", key=f"cancel_{order.get('id')}"):
                        cancel_result = api_request("PUT", f"/orders/{order.get('id')}/cancel")
                        if cancel_result and cancel_result.get("success"):
                            st.success(f"Sipariş #{order.get('id')} iptal edildi!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"İptal başarısız: {cancel_result}")

# ==================== TAB 3: KARGO TAKİBİ ====================
with tab3:
    st.subheader("🚚 Kargo Takibi")
    
    # Önce siparişleri getir
    orders_response = api_request("GET", "/orders/my")
    
    if orders_response:
        if isinstance(orders_response, list):
            orders = orders_response
        elif isinstance(orders_response, dict) and orders_response.get("success"):
            orders = orders_response.get("data", [])
        elif isinstance(orders_response, dict) and orders_response.get("data"):
            orders = orders_response.get("data", [])
        else:
            orders = []
    else:
        orders = []
    
    if orders:
        # Sadece kargolanmış siparişleri göster
        shipped_orders = [o for o in orders if o.get('status') in ['shipped', 'delivered', 'completed', 'cargo']]
        
        if shipped_orders:
            selected_order = st.selectbox(
                "Kargosunu görmek istediğiniz siparişi seçin:",
                options=shipped_orders,
                format_func=lambda x: f"Sipariş #{x.get('id')} - {x.get('status')}"
            )
            
            if selected_order:
                order_id = selected_order.get('id')
                shipment_response = api_request("GET", f"/shipments/order/{order_id}")
                
                if shipment_response and shipment_response.get("success"):
                    shipment = shipment_response.get("data")
                    if shipment:
                        st.success("📦 Kargo bilgileri bulundu!")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Takip Numarası", shipment.get('tracking_number', '-'))
                            st.metric("Kargo Şirketi", shipment.get('cargo_company', shipment.get('carrier', '-')))
                        with col2:
                            st.metric("Durum", shipment.get('status', '-'))
                    else:
                        st.info("Bu sipariş için henüz kargo oluşturulmamış.")
                else:
                    st.info("Bu sipariş için henüz kargo bilgisi girilmemiş.")
        else:
            st.info("Kargolanmış siparişiniz bulunmuyor.")
    else:
        st.info("Önce sipariş oluşturmalısınız.")
# ==================== TAB 4: AI MÜŞTERİ ASİSTANI ====================
with tab4:
    st.subheader("🤖 AI Müşteri Asistanı")
    st.caption("💡 Bana sorabilirsiniz: Siparişim nerede? | Kaç siparişim var? | Stokta X var mı? | Kargo gecikti mi?")
    
    # Chat geçmişi için session state
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []
    
    # Chat geçmişini göster
    for msg in st.session_state.ai_messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Sorunuzu yazın..."):
        # Kullanıcı mesajını ekle
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Backend'e soruyu gönder - AI endpoint'i
        response = api_request("POST", "/ai/customer-chat", {"message": prompt})
        
        # Response'u işle - backend'iniz direkt mesaj dönüyor (wrapped değil)
        if response:
            if isinstance(response, dict):
                # Eğer hata varsa
                if "error" in response:
                    answer = f"❌ Hata: {response.get('error')}"
                # Eğer doğrudan message field'ı varsa
                elif "message" in response:
                    answer = response.get("message")
                # Eğer success/data formatındaysa
                elif response.get("success") and response.get("data"):
                    answer = response.get("data")
                else:
                    answer = str(response)
            else:
                answer = str(response)
        else:
            answer = "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
        
        # Asistan yanıtını ekle
        st.session_state.ai_messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)
        
        # Scroll için rerun
        st.rerun()