# Backend API SIGANTENG

Layanan backend ini dibangun menggunakan **FastAPI** dan dirancang dengan arsitektur modern untuk menangani tugas-tugas AI yang kompleks secara asinkron.

## Arsitektur & Pola Desain

Backend ini tidak hanya sekadar API, tetapi sebuah sistem yang dirancang untuk keandalan dan skalabilitas, menggunakan beberapa pola desain utama:

1.  **Arsitektur Asinkron dengan Celery & Redis**:
    - **Masalah**: Tugas AI (seperti memanggil model bahasa atau mengubah teks menjadi suara) bisa memakan waktu lama dan akan menyebabkan *timeout* jika ditangani secara sinkron dalam permintaan HTTP.
    - **Solusi**: Kami menggunakan **Celery** sebagai *task queue* dan **Redis** sebagai *message broker*. Saat permintaan untuk tugas berat masuk, API hanya menempatkan tugas di antrian dan segera mengembalikan `task_id` kepada klien. **Celery Worker**, yang berjalan sebagai proses terpisah, akan mengambil tugas tersebut dan mengerjakannya di latar belakang.

2.  **Pola Desain Adapter**:
    - **Masalah**: Mengikat kode layanan secara langsung ke satu penyedia AI (misalnya, hanya OpenAI) membuatnya sulit untuk diganti atau dikembangkan.
    - **Solusi**: Kami menggunakan *Adapter Pattern*. Untuk setiap jenis layanan AI (LLM, Vision, TTS, dll.), kami mendefinisikan sebuah *interface* dasar (misalnya, `BaseLLMAdapter`). Kemudian, kami membuat implementasi konkret untuk setiap penyedia (`OpenAILLMAdapter`, `HuggingFaceLLMAdapter`). *Service layer* (misalnya, `LLMService`) kemudian menggunakan *interface* ini, sehingga penyedia model dapat diganti dengan mudah melalui konfigurasi tanpa mengubah logika bisnis.

3.  **Dependency Injection**:
    - **Masalah**: Membuat instance layanan secara global dapat menyebabkan masalah saat pengujian (misalnya, mencoba terhubung ke database saat tes dikumpulkan).
    - **Solusi**: Kami memanfaatkan sistem *Dependency Injection* bawaan FastAPI (`Depends`). Layanan diinisialisasi per permintaan, memungkinkan kami untuk dengan mudah menggantinya dengan *mock object* selama pengujian.

## Alur Kerja API Non-Blocking

Untuk tugas yang berjalan lama, alur kerjanya adalah sebagai berikut:

1.  **`POST /background/generate_text`**:
    - Klien mengirimkan *prompt*.
    - API memvalidasi input dan memanggil `AIOrchestratorService` untuk mengirimkan tugas ke Celery.
    - API segera merespons dengan `HTTP 202 Accepted` dan sebuah `task_id`.

2.  **`GET /background/tasks/{task_id}`**:
    - Klien menggunakan `task_id` untuk secara berkala (polling) menanyakan status tugas.
    - API akan merespons dengan status (`PENDING`, `SUCCESS`, `FAILURE`) dan hasilnya jika sudah tersedia.

## Setup & Menjalankan Lokal

### Prasyarat

- Python 3.11+
- Docker (untuk menjalankan Redis)

### Langkah-langkah

1.  **Navigasi & Buat Virtual Environment**
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # atau .venv\Scripts\activate di Windows
    ```

2.  **Install Dependensi**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Konfigurasi Environment**
    - Salin `backend/.env.example` menjadi `backend/.env`.
    - Isi semua variabel yang diperlukan (Database, Redis, API Keys, dll.).

4.  **Jalankan Layanan Pendukung (Redis)**
    Buka terminal dan jalankan Redis menggunakan Docker.
    ```bash
    docker run -d -p 6379:6379 redis:7
    ```

5.  **Jalankan Aplikasi (API & Worker)**
    Anda memerlukan **dua terminal terpisah** di dalam direktori `backend` yang sudah teraktivasi *virtual environment*-nya.

    **Terminal 1: Jalankan Celery Worker**
    ```bash
    celery -A app.core.celery_app.celery_app worker --loglevel=info
    ```
    Worker ini akan memantau dan mengerjakan tugas dari antrian Redis.

    **Terminal 2: Jalankan API Server**
    ```bash
    uvicorn main:app --reload
    ```
    Server API akan aktif di `http://localhost:8000`. Dokumentasi interaktif (Swagger UI) tersedia di `http://localhost:8000/docs`.
