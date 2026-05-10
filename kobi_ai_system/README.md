# 🚀 KOBİ-AI (AI Microservice)
### Yapay Zeka & Multi-Agent Modülü

Bu repo, **Takım 172** projesi olan KOBİ-AI'nin **Yapay Zeka ve Ajan (Agent)** modülünü içermektedir. Projenin ana frontend ve backend'inden bağımsız bir **AI Microservice** olarak çalışacak şekilde tasarlanmıştır.

Frontend ve Backend ekiplerindeki ekip arkadaşlarım bu repoyu klonlayarak AI asistan servislerini kendi lokal ortamlarında çalıştırabilir ve API uç noktaları üzerinden projeye entegre edebilirler.

---

## 📌 İçindekiler
- [Genel Bakış](#-genel-bakış)
- [Teknolojik Stack](#-teknolojik-stack)
- [Ekip Arkadaşları İçin Kurulum](#-ekip-arkadaşları-için-kurulum)
- [Uygulamayı Çalıştırma](#-uygulamayı-çalıştırma)
- [Frontend / Backend İçin API Kullanımı](#-frontend--backend-için-api-kullanımı)
- [Proje Klasör Yapısı](#-proje-klasör-yapısı)

---

## 🧩 Genel Bakış

Bu modül, LangGraph ve Gemini 2.5 modellerini kullanarak KOBİ'lerin operasyonel sorularını yanıtlayan iki ana yapay zeka ajanını (Agent) barındırır:

1. **Orchestrator Agent (`/api/chat`):** Müşteri paneli için. Stok durumu, kargo takibi ve şirket politikaları (RAG) konularında yanıt üretir.
2. **Analytics Agent (`/api/admin/chat`):** Yönetici paneli için. Satış verileri, ciro raporları ve operasyon analitiği yapar.

Ajanlar her zaman diğer modüllerin (Frontend) rahatça işleyebileceği yapılandırılmış **JSON** formatında döner.

---

## 💻 Teknolojik Stack

- **Framework:** FastAPI, Uvicorn
- **AI Frameworks:** LangChain, LangGraph
- **Modeller:** Google Gemini 2.5 Flash, Gemini 2.5 Flash Lite, Google Generative AI Embeddings
- **Vektör Veritabanı:** FAISS
- **Ortam:** Python 3.10+

---

## 🛠️ Ekip Arkadaşları İçin Kurulum

Bu projeyi kendi bilgisayarınıza klonladıktan sonra şu adımları izleyin:

### 1. Ortamı Kurun ve Bağımlılıkları Yükleyin

```bash
# Repoyu klonlayın ve klasöre girin
# (Örnek: git clone <repo_url> && cd kobi_ai_system)

# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktif edin (Windows)
.\venv\Scripts\activate
# (Mac/Linux kullananlar için: source venv/bin/activate)

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

### 2. Çevre Değişkenleri (.env)

Proje kök dizininde `.env` isimli bir dosya oluşturun. Test edebilmeniz için Gemini API anahtarını buraya ekleyin:

```env
GEMINI_API_KEY="BURAYA_GOOGLE_AI_STUDIO_ANAHTARINIZI_YAZIN"
```

### 3. Vektör Veritabanını (RAG) Hazırlama

Ajanın kurumsal şirket kurallarını (iade politikası vs.) okuyabilmesi için FAISS veritabanının oluşturulması gereklidir. Kurulum sonrası **bir kereye mahsus** şu komutu çalıştırın:

```bash
python -m app.rag.ingestion
```
*(Not: Bu komutu çalıştırdığınızda kodların olduğu yerde otomatik olarak bir `data/` klasörü oluşacaktır. Az önce bahsettiğimiz klasör budur, FAISS veritabanı buraya kaydedilir ve .gitignore'a eklidir, GitHub'dan gelmez.)*

---

## 🚀 Uygulamayı Çalıştırma

Gerekli kurulumları yaptıktan sonra AI servisini başlatmak için:

```bash
uvicorn app.main:app --reload
```

Sistem `http://127.0.0.1:8000` portunda ayağa kalkacaktır.

---

## 📡 Frontend / Backend İçin API Kullanımı

Sistemimiz UI tarafında kolay render edilebilmesi için JSON formatında yanıt döndürür. Etkileşimli dokümantasyon (Swagger UI) için `http://127.0.0.1:8000/docs` adresini inceleyebilirsiniz.

### 1. Müşteri Soruları (Orchestrator Agent)
**Endpoint:** `POST /api/chat`

**Örnek İstek Gövdesi (Request Body):**
```json
{
  "message": "Sipariş durumum nedir?",
  "session_id": "test_session_123"
}
```

**Örnek Yanıt (Response):**
```json
{
  "message": "Müşteriye gösterilecek metin yanıtı...",
  "ui_type": "cargo_timeline", 
  "ui_data": {} // Frontend'in komponent çizmek için kullanacağı ek veriler
}
```

### 2. Yönetici Soruları (Analytics Agent)
**Endpoint:** `POST /api/admin/chat`

**Örnek İstek Gövdesi:**
```json
{
  "message": "Bugün işler nasıldı, ciro ne kadar?",
  "session_id": "admin_session_456"
}
```

**Örnek Yanıt:**
```json
{
  "message": "Yöneticiye gösterilecek özet rapor...",
  "ui_type": "sales_dashboard",
  "ui_data": {} // Dashboard widgetları için veriler
}
```
*(Not: Frontend geliştirici arkadaşımız dönen yanıttaki `ui_type` alanına bakarak ('text', 'cargo_timeline', 'product_card', 'sales_dashboard' vb.) uygun arayüz bileşenini ekranda çizebilir.)*

---

## 📁 Proje Klasör Yapısı

```text
kobi_ai_system/
├── app/
│   ├── agents/          # Yapay zeka ajanları (Orchestrator, Analytics)
│   ├── core/            # Ayarlar ve konfigürasyon
│   ├── rag/             # Vektör DB (FAISS) oluşturma ve okuma işlemleri
│   ├── schemas/         # Pydantic modelleri (API İstek/Yanıt formatları)
│   ├── tools/           # Ajanların yetenekleri (Stok sorgulama, Kargo arama vs.)
│   ├── utils/           # Log mekanizmaları ve hatalar
│   └── main.py          # AI servisi FastAPI başlangıç noktası
├── requirements.txt     # Bağımlılık listesi
└── README.md            # Bu dosya
```