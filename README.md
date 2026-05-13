<div align="center">
  <h1>🚀 Takım 172: Akıllı KOBİ Asistanı ve E-Ticaret Platformu</h1>
  <p><strong>Yapay Zeka Destekli Yeni Nesil Satış ve Müşteri İlişkileri Yönetimi</strong></p>
</div>

---

## 📌 Projenin Amacı ve Vizyonu

Günümüzde KOBİ'ler (Küçük ve Orta Büyüklükteki İşletmeler), dijitalleşme sürecinde müşteri destek operasyonları ve veri analitiği konularında ciddi zorluklar yaşamaktadır. **Takım 172**, KOBİ'lerin bu yükünü hafifletmek amacıyla geliştirilmiş **uçtan uca bir e-ticaret ve akıllı yapay zeka** platformudur. 

Projemiz, standart bir alışveriş deneyimini **LangGraph** ve **Gemini 2.5** modelleriyle güçlendirilmiş otonom bir AI mikroservisi ile birleştirir. Müşterileriniz yapay zeka ile 7/24 kesintisiz iletişim kurarken, siz (yönetici) arka planda satışlarınızı ve analitik verilerinizi yine yapay zekaya sorarak saniyeler içinde raporlayabilirsiniz.

## 🌟 Öne Çıkan Özellikler (Jüri İçin Özet)

### 1. 🤖 Çoklu Ajan (Multi-Agent) Yapay Zeka Mimarisi
Sistemimiz basit bir "soru-cevap" botu değil, **LangGraph** altyapısında çalışan araç-kullanabilen (Tool-Calling) otonom ajanlardan oluşur:
*   **Orchestrator Agent (Müşteri İçin):** Gerçek zamanlı veritabanına bağlanıp kullanıcının kargosunun nerede olduğunu bulur, stok ve fiyat sorgulaması yapar.
*   **Analytics Agent (Yönetici İçin):** Yöneticinin "Bugün işler nasıldı?" sorusu üzerine veritabanından satış verilerini çeker, geciken kargoları tespit eder ve anlamlı iş raporları sunar.

### 2. 📚 RAG (Retrieval-Augmented Generation) Entegrasyonu
KOBİ'lerin sıkça değişen "İade Politikası", "Çalışma Saatleri" gibi kurum içi kuralları **FAISS Vektör Veritabanı** kullanılarak modellere entegre edilmiştir. Yapay zeka, doğrudan şirketin belgelerinden okuyarak sıfır halüsinasyon (hallucination) ile cevap verir.

### 3. ⚡ Modern ve Hızlı Mimari
Uygulamamız mikroservis mantığıyla ayrılmış, ancak tek bir çatı altında kusursuzca birleştirilmiştir. Frontend tarafı React ile modern ve pürüzsüz bir arayüz sunarken, Backend tarafı FastAPI sayesinde asenkron ve ultra hızlı yanıtlar verir.

---

## 🛠️ Kullanılan Teknolojiler

**Frontend (Kullanıcı Arayüzü):**
*   **React 19 & TypeScript:** Güvenli, tip kontrollü ve modern UI bileşenleri.
*   **Vite:** Ultra hızlı geliştirme ortamı ve build süreci.

**Backend (Sunucu ve API):**
*   **FastAPI:** Asenkron destekli, yüksek performanslı Python API iskeleti.
*   **SQLAlchemy & PostgreSQL:** Güçlü, ilişkisel veritabanı yönetimi ve ORM mimarisi.
*   **JWT (JSON Web Token):** Güvenli yetkilendirme ve rol yönetimi.

**Kobi AI System (Yapay Zeka Modülü):**
*   **LangChain & LangGraph:** Multi-agent (çoklu ajan) yönlendirmesi ve hafıza (memory) yönetimi.
*   **Google Gemini 2.5 Flash / Flash-Lite:** Mantıksal çıkarım ve doğal dil işleme görevleri.
*   **Google Embeddings & FAISS:** Vektörel veri arama ve RAG süreçleri.

---

## 📂 Proje Klasör Yapısı

```text
Takim172/
│
├── frontend/             # Müşteri ve Yönetici Web Arayüzü (React)
│   ├── src/components    # UI Bileşenleri (Sohbet, Ürün Kartları)
│   ├── src/pages         # Ana Sayfalar
│   └── package.json      # Frontend bağımlılıkları
│
├── backend/              # Ana İş Mantığı ve Veritabanı Yönetimi (FastAPI)
│   ├── app/api/routes    # Ürünler, Siparişler, Kullanıcılar ve AI Uç Noktaları
│   ├── app/models        # SQLAlchemy Veritabanı Şemaları
│   ├── app/schemas       # Pydantic Veri Doğrulama Modelleri
│   └── requirements.txt  # Python bağımlılıkları
│
└── kobi_ai_system/       # Yapay Zeka Mikroservisi Çekirdeği
    ├── app/agents        # Orchestrator ve Analytics ajanlarının karar mekanizmaları
    ├── app/tools         # AI'nin kullandığı araçlar (Kargo sorgula, Stok kontrolü)
    ├── app/rag           # Vektör DB (FAISS) oluşturma mantığı
    └── data/             # RAG İndex Dosyaları
```

---

## 🚀 Yerel Ortamda Çalıştırma Adımları (Kurulum)

Projeyi kendi bilgisayarınızda ayağa kaldırmak oldukça basittir. İki ayrı terminal kullanarak sistemi başlatabilirsiniz.

### 1. Ana Sunucu ve Yapay Zeka Servisini Başlatma (Backend)
Projeyi klonladıktan sonra root (ana) dizinde bir terminal açın:

```bash
# Sanal ortam oluşturma ve aktif etme
python -m venv backend\venv
.\backend\venv\Scripts\activate   # Windows için

# Gerekli tüm backend ve yapay zeka kütüphanelerini kurma
pip install -r backend\requirements.txt
pip install -r kobi_ai_system\requirements.txt

# Çevresel değişkeni ayarlama (Varsa .env dosyanıza ekleyin)
# GEMINI_API_KEY="SİZİN_GOOGLE_API_ANAHTARINIZ"

# Sunucuyu başlatma
uvicorn backend.app.main:app --reload --port 8080
```

### 2. Kullanıcı Arayüzünü Başlatma (Frontend)
Yeni bir terminal açın ve `frontend` klasörüne girin:

```bash
cd frontend

# Bağımlılıkları yükleme
npm install

# React uygulamasını başlatma
npm run dev
```

Uygulamanız artık `http://localhost:5173` adresinde yayında olacaktır!

---

## 🎯 Jürinin Dikkatine

Değerli jüri üyeleri; projemizi incelerken lütfen sağ alt köşedeki **✨ KOBİ-AI Sor** butonunu test etmeyi unutmayın. Yapay zekaya şu tarz sorular sorarak sistemin RAG ve Tool-Calling yeteneklerini bizzat deneyimleyebilirsiniz:
*   *"Sırt çantasından stoklarınızda var mı? Fiyatı ne kadar?"* (Veritabanından canlı veri okur)
*   *"Siparişim nerede kaldı?"* (Kargo durum sorgulama aracını çalıştırır)
*   *"İade politikanız nedir?"* (RAG modülü ile kurumsal belgelerden okuma yapar)

**Takım 172**, geleceğin otonom e-ticaret dünyasına hazırdır!
