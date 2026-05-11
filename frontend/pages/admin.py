import streamlit as st
from services.api import api_request
import time
import pandas as pd

st.set_page_config(
    page_title="Admin Paneli",
    page_icon="👑",
    layout="wide"
)

# Yetki kontrolü
if not st.session_state.get("token"):
    st.warning("Lütfen önce giriş yapın.")
    st.switch_page("login.py")

if st.session_state.get("role") != "admin":
    st.error("Bu sayfaya erişim yetkiniz yok. Bu sayfa sadece adminler içindir.")
    st.stop()

st.sidebar.title(f"👑 Hoş geldin, {st.session_state.get('username', 'Admin')}")
st.sidebar.markdown("---")

# Ana sekmeler
tab1, tab2, tab3 = st.tabs([
    "👥 Kullanıcı Yönetimi",
    "🏪 Satıcı Yönetimi",
    "📊 Dashboard"
])

# ==================== TAB 1: KULLANICI YÖNETİMİ ====================
with tab1:
    st.subheader("👥 Kullanıcı Yönetimi")
    
    # Kullanıcıları getir
    users_response = api_request("GET", "/users")
    
    if users_response and users_response.get("success"):
        users = users_response.get("data", [])
        
        if users:
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
            
            # Kullanıcı tablosu
            st.subheader("📋 Kullanıcı Listesi")
            
            # Arama filtresi
            search = st.text_input("🔍 E-posta ile ara", placeholder="kullanici@email.com")
            
            filtered_users = users
            if search:
                filtered_users = [u for u in users if search.lower() in u.get("email", "").lower()]
            
            # Tablo gösterimi
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
                        st.caption(f"Kayıt: {user.get('created_at', '')[:10] if user.get('created_at') else '-'}")
                    
                    with col4:
                        # Rol değiştirme (kendini değiştirmesin)
                        if user.get('email') != st.session_state.get('email'):
                            current_role = user.get('role', 'user')
                            new_role = st.selectbox(
                                "Yeni Rol",
                                options=["user", "seller", "admin"],
                                index=["user", "seller", "admin"].index(current_role) if current_role in ["user", "seller", "admin"] else 0,
                                key=f"role_{user.get('id')}",
                                label_visibility="collapsed"
                            )
                            
                            if new_role != current_role:
                                if st.button("💾 Kaydet", key=f"save_role_{user.get('id')}"):
                                    update_response = api_request(
                                        "PUT", 
                                        f"/users/{user.get('id')}/role?role={new_role}",
                                        None
                                    )
                                    
                                    if update_response and update_response.get("success"):
                                        st.success("Güncellendi!")
                                        st.rerun()
                                    else:
                                        st.error("Hata!")
                        else:
                            st.info("👑 Kendi rolün")
                    
                    with col5:
                        if user.get('email') != st.session_state.get('email'):
                            if st.button("🗑️ Sil", key=f"delete_{user.get('id')}"):
                                # Not: Silme onayı için expander yerine bir modal veya state yönetimi daha sağlıklı olabilir
                                # ancak mevcut mantıkta expander kullanımı düzenlendi.
                                delete_response = api_request("DELETE", f"/users/{user.get('id')}")
                                if delete_response and delete_response.get("success"):
                                    st.success("Silindi!")
                                    st.rerun()
                                else:
                                    st.error("Hata!")
        else:
            st.info("Henüz kullanıcı bulunmuyor.")
    else:
        st.error("Kullanıcılar yüklenemedi!")

# ==================== TAB 2: SATICI YÖNETİMİ ====================
with tab2:
    st.subheader("🏪 Satıcı Yönetimi")
    sellers_response = api_request("GET", "/sellers")
    
    if sellers_response and sellers_response.get("success"):
        sellers = sellers_response.get("data", [])
        if sellers:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Satıcı", len(sellers))
            with col2:
                avg_rating = sum(s.get("rating", 0) for s in sellers) / len(sellers) if sellers else 0
                st.metric("Ortalama Puan", f"{avg_rating:.1f}/5")
            with col3:
                products_response = api_request("GET", "/products")
                total_products = len(products_response.get("data", [])) if products_response and products_response.get("success") else 0
                st.metric("Toplam Ürün", total_products)
            
            st.markdown("---")
            search_seller = st.text_input("🔍 Mağaza adı ile ara", key="seller_search")
            filtered_sellers = [s for s in sellers if search_seller.lower() in s.get("store_name", "").lower()] if search_seller else sellers
            
            for seller in filtered_sellers:
                with st.expander(f"🏪 {seller.get('store_name', 'İsimsiz Mağaza')} - ⭐ {seller.get('rating', 0)}/5"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Mağaza Adı:** {seller.get('store_name')}")
                        st.markdown(f"**Açıklama:** {seller.get('description', 'Açıklama yok')}")
                    
                    with col2:
                        current_rating = seller.get('rating', 0)
                        new_rating = st.slider("⭐ Puan", 0, 5, int(current_rating), key=f"rating_{seller.get('id')}")
                        if new_rating != current_rating:
                            if st.button("💾 Puanı Güncelle", key=f"update_rating_{seller.get('id')}"):
                                update_data = {
                                    "store_name": seller.get('store_name'),
                                    "description": seller.get('description'),
                                    "rating": new_rating
                                }
                                update_response = api_request("PUT", f"/sellers/{seller.get('id')}", update_data)
                                if update_response and update_response.get("success"):
                                    st.success("Puan güncellendi!")
                                    st.rerun()

# ==================== TAB 3: DASHBOARD ====================
with tab3:

    st.subheader("📊 Admin Dashboard")

   

    # Genel istatistikler

    col1, col2, col3, col4 = st.columns(4)

   

    # Kullanıcı istatistiği

    users_response = api_request("GET", "/users")

    total_users = 0

    if users_response and users_response.get("success"):

        users = users_response.get("data", [])

        total_users = len(users)

        user_count = len([u for u in users if u.get("role") == "user"])

        seller_count = len([u for u in users if u.get("role") == "seller"])

    else:

        user_count = 0

        seller_count = 0

   

    with col1:

        st.metric("Toplam Kullanıcı", total_users)

    with col2:

        st.metric("Aktif Müşteriler", user_count)

    with col3:

        st.metric("Aktif Satıcılar", seller_count)

    with col4:

        # Sipariş istatistiği

        orders_response = api_request("GET", "/orders")

        total_orders = 0

        if orders_response and orders_response.get("success"):

            total_orders = len(orders_response.get("data", []))

        st.metric("Toplam Sipariş", total_orders)

   

    st.markdown("---")

   

    # Ürün istatistiği

    st.subheader("📦 Ürün İstatistikleri")

   

    products_response = api_request("GET", "/products")

    if products_response and products_response.get("success"):

        products = products_response.get("data", [])

       

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric("Toplam Ürün", len(products))

        with col2:

            total_stock = sum(p.get("stock", 0) for p in products)

            st.metric("Toplam Stok", total_stock)

        with col3:

            avg_price = sum(p.get("price", 0) for p in products) / len(products) if products else 0

            st.metric("Ortalama Fiyat", f"{avg_price:.2f} TL")

       

        # En çok satan ürünler

        st.subheader("🔥 En Çok Satan Ürünler")

       

        orders_response = api_request("GET", "/orders")

        if orders_response and orders_response.get("success"):

            orders = orders_response.get("data", [])

           

            # Ürün bazında satış adedi hesapla

            product_sales = {}

            for order in orders:

                product_id = order.get("product_id")

                quantity = order.get("quantity", 0)

                product_sales[product_id] = product_sales.get(product_id, 0) + quantity

           

            # Ürün detaylarıyla birleştir

            product_stats = []

            for product in products:

                product_id = product.get("id")

                product_stats.append({

                    "name": product.get("name"),

                    "price": product.get("price"),

                    "stock": product.get("stock"),

                    "sales": product_sales.get(product_id, 0),

                    "revenue": product_sales.get(product_id, 0) * product.get("price", 0)

                })

           

            # Satışa göre sırala

            product_stats.sort(key=lambda x: x["sales"], reverse=True)

           

            # Top 10 göster

            for idx, p in enumerate(product_stats[:10]):

                with st.container(border=True):

                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                    with col1:

                        st.markdown(f"**{idx+1}. {p['name']}**")

                    with col2:

                        st.metric("Fiyat", f"{p['price']} TL")

                    with col3:

                        st.metric("Satış Adedi", p['sales'])

                    with col4:

                        st.metric("Ciro", f"{p['revenue']} TL")

    else:

        st.info("Ürün verisi alınamadı.")

   

    st.markdown("---")

   

    # Son aktiviteler

    st.subheader("📋 Son Aktiviteler")

   

    # Son siparişler

    orders_response = api_request("GET", "/orders")

    if orders_response and orders_response.get("success"):

        orders = orders_response.get("data", [])

        if orders:

            st.markdown("**Son 10 Sipariş:**")

            recent_orders = sorted(orders, key=lambda x: x.get("created_at", ""), reverse=True)[:10]

           

            orders_df = pd.DataFrame(recent_orders)

            st.dataframe(

                orders_df[['id', 'user_id', 'product_id', 'quantity', 'status', 'created_at']],

                use_container_width=True

            )

        else:

            st.info("Henüz sipariş yok.")