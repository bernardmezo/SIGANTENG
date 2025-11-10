# SIGANTENG - Asisten AI Kreatif Multimodal

Selamat datang di SIGANTENG, sebuah proyek portofolio yang mendemonstrasikan arsitektur aplikasi AI modern yang andal dan skalabel. SIGANTENG dirancang untuk memberikan pengalaman interaktif melalui orkestrasi *background jobs* untuk tugas-tugas AI yang kompleks.

## ✨ Fitur Utama

- **Arsitektur Asinkron**: Menggunakan **Celery** dan **Redis** untuk menangani tugas AI yang berat (seperti generasi gambar atau teks) di latar belakang, memastikan API tetap responsif.
- **Pola Desain Adapter**: Memisahkan logika bisnis dari implementasi model AI spesifik, memungkinkan sistem untuk beralih antara penyedia layanan (misalnya, OpenAI ke Hugging Face) dengan mudah.
- **"Wow Moment"**: Alur kerja orkestrasi AI yang kompleks:
    1.  **Unggah Gambar**: Pengguna mengunggah gambar.
    2.  **Analisis & Puisi**: *Background job* menganalisis gambar dan menghasilkan puisi.
    3.  **Narasi Suara**: *Background job* lain mengubah puisi menjadi narasi suara.
- **API Non-Blocking**: Klien (frontend) dapat mengirim permintaan *job* dan menerima `task_id` untuk memeriksa statusnya nanti, mencegah *timeout* HTTP.

## 🚀 Tumpukan Teknologi (Tech Stack)

Arsitektur SIGANTENG dibangun di atas tumpukan teknologi modern yang dipilih untuk skalabilitas dan kemudahan deployment.

| Kategori | Teknologi | Platform Deployment |
| :--- | :--- | :--- |
| **Frontend** | Next.js, TypeScript, Tailwind CSS | **Vercel** |
| **Backend API** | FastAPI, Python | **Render** |
| **Background Worker** | Celery, Python | **Render** |
| **Database** | PostgreSQL | **Neon** |
| **Message Broker** | Redis | **Render** |
| **Autentikasi** | Clerk | Clerk |
| **Penyimpanan File** | Cloudinary | Cloudinary |

## 🛠️ Memulai Proyek Secara Lokal

### Prasyarat

- Node.js (v20+)
- Python (v3.11+)
- Docker (untuk menjalankan Redis dengan mudah)
- Akun di [Neon](https://neon.tech/), [Clerk](https://clerk.com/), [Cloudinary](https://cloudinary.com/), dan [OpenAI](https://openai.com/).

### 1. Kloning & Konfigurasi

```bash
git clone https://github.com/username/siganteng.git
cd siganteng

# Salin file environment backend
cp backend/.env.example backend/.env

# Salin variabel frontend ke file environment-nya sendiri
# (Buat file frontend/.env.local dan salin bagian frontend dari backend/.env.example)
```
Buka `backend/.env` dan isi **semua** variabel dengan kredensial Anda.

### 2. Menjalankan Layanan Backend

Buka 3 terminal terpisah.

**Terminal 1: Jalankan Redis (via Docker)**
```bash
docker run -d -p 6379:6379 redis:7
```

**Terminal 2: Jalankan Backend API & Worker**
```bash
# Arahkan ke direktori backend
cd backend

# Buat dan aktifkan virtual environment
python -m venv .venv
source .venv/bin/activate  # atau .venv\Scripts\activate di Windows

# Install dependensi
pip install -r requirements.txt

# Jalankan Celery Worker
celery -A app.core.celery_app.celery_app worker --loglevel=info

# Jalankan API Server (di terminal lain)
uvicorn main:app --reload
```
- API akan berjalan di `http://localhost:8000`.
- Celery worker sekarang memantau tugas baru.

### 3. Menjalankan Frontend

**Terminal 3: Jalankan Frontend**
```bash
# Arahkan ke direktori frontend
cd frontend

# Install dependensi
npm install

# Jalankan server pengembangan
npm run dev
```
- Frontend akan berjalan di `http://localhost:3000`.

## 📂 Struktur Proyek

Proyek ini memiliki struktur monorepo dengan dua direktori utama: `frontend` dan `backend`.

- **`/frontend`**: Aplikasi Next.js yang menangani semua antarmuka pengguna.
- **`/backend`**: API FastAPI yang berisi semua logika backend, termasuk:
    - **`app/api/`**: Definisi endpoint.
    - **`app/services/`**: Logika bisnis dan implementasi pola Adapter.
    - **`app/core/`**: Konfigurasi aplikasi, Celery, dan pengaturan lainnya.
    - **`app/tasks.py`**: Definisi tugas-tugas yang akan dijalankan oleh Celery.
- **`/DEVELOPMENT_PLAN.md`**: Dokumen utama yang menjadi pedoman pengembangan proyek ini.
