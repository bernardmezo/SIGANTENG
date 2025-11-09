# Backend API SIGANTENG

Ini adalah layanan backend yang dibangun menggunakan FastAPI untuk proyek SIGANTENG. Backend ini bertanggung jawab atas semua logika bisnis, orkestrasi model AI, dan interaksi dengan database.

## Fitur Utama

- **API Berbasis REST**: Menyediakan endpoint yang jelas dan terstruktur untuk semua kebutuhan frontend.
- **Orkestrasi AI**: Mengelola alur kompleks "Wow Moment" dari pemrosesan gambar hingga sintesis suara.
- **Terintegrasi dengan Layanan Eksternal**: Terhubung dengan database Neon, autentikasi Clerk, dan penyimpanan Cloudinary.

## Endpoints API

Dokumentasi API interaktif (Swagger UI) tersedia di `/docs` saat server berjalan.

- `POST /api/v1/ai/chat`: Endpoint untuk interaksi chat sederhana.
- `POST /api/v1/ai/wow-moment`: Endpoint untuk orkestrasi "Wow Moment" (gambar -> puisi -> suara).
- `GET /api/v1/kb/search`: (Placeholder) Endpoint untuk pencarian di knowledge base.

## Tumpukan Teknologi & Model AI

Backend ini menggunakan FastAPI dan Pydantic untuk performa dan validasi data yang solid. Kekuatan utamanya terletak pada integrasi dengan model-model AI *open-source* yang dipilih secara cermat, dengan penekanan pada pemahaman Bahasa Indonesia.

- **Framework**: FastAPI
- **Bahasa**: Python 3.11+
- **Validasi Data**: Pydantic

### Model AI yang Digunakan

Berikut adalah daftar model yang menjadi inti dari layanan AI kami:

| Fungsi | Model | Peran dalam Layanan |
| :--- | :--- | :--- |
| **Visi (CV)** | `Salesforce/blip-image-captioning-base` | Menerjemahkan gambar menjadi deskripsi teks sebagai dasar pembuatan puisi. |
| **Generator Puisi** | `cahya/gpt2-small-indonesian` | Mengambil deskripsi gambar dan prompt untuk menghasilkan puisi kreatif. |
| **Analisis Sentimen**| `indobenchmark/indobert-base-p2` | Memahami nuansa emosional dari input teks untuk respons yang lebih baik. |
| **ASR (Suara → Teks)**| `openai/whisper-base` | Mengonversi input audio dari pengguna menjadi teks yang dapat diproses. |
| **TTS (Teks → Suara)**| `facebook/mms-tts-ind` | Mengubah teks puisi yang dihasilkan menjadi narasi suara berbahasa Indonesia. |
| **Embeddings** | `all-MiniLM-L6-v2` | *(Untuk pengembangan masa depan)* Akan digunakan untuk membangun *Knowledge Base* dengan pencarian semantik. |

## Setup Lokal

### Prasyarat

- Python 3.11+
- Pip (package installer)

### Langkah-langkah

1.  **Navigasi ke Direktori Backend**
    ```bash
    cd backend
    ```

2.  **Buat dan Aktifkan Virtual Environment** (Disarankan)
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependensi**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Environment**
    Pastikan Anda sudah menyalin `backend/.env.example` menjadi `backend/.env` dan mengisinya dengan kredensial yang benar.

5.  **Jalankan Server**
    ```bash
    uvicorn app.main:app --reload
    ```
    Server akan aktif di `http://localhost:8000`.

## Arsitektur Layanan

Backend dirancang dengan arsitektur berorientasi layanan (*service-oriented*) untuk memisahkan setiap tugas ke dalam modulnya sendiri, membuatnya lebih mudah untuk dikelola dan diskalakan.

- **`app/api/`**: Mendefinisikan semua endpoint API.
- **`app/services/`**: Berisi logika inti untuk setiap fungsionalitas (misalnya, `vision_service.py`, `tts_service.py`).
- **`app/core/`**: Mengelola konfigurasi dan dependensi inti.
- **`app/models/`**: (Placeholder) Skema data dan interaksi database.

Model AI diunduh dan di-cache secara otomatis pada saat pertama kali layanan dijalankan. Pastikan Anda memiliki koneksi internet yang stabil saat pertama kali menjalankan.