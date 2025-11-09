# SIGANTENG - Asisten AI Kreatif Anda

Selamat datang di SIGANTENG, sebuah proyek portofolio yang mendemonstrasikan kekuatan asisten AI multimodal. SIGANTENG dirancang untuk memberikan pengalaman interaktif yang memukau melalui dua alur utama: **"Magic Moment"** untuk interaksi instan tanpa login, dan **"Wow Moment"** yang mengubah gambar menjadi puisi dan narasi suara.

## ✨ Fitur Utama

- **Magic Moment**: Coba langsung kemampuan chat AI tanpa perlu mendaftar. Pengalaman pertama yang mulus dan tanpa friksi.
- **Wow Moment**: Orkestrasi AI yang kompleks:
    1.  **Unggah Gambar**: Pilih gambar apa pun yang menginspirasi Anda.
    2.  **Puisi Otomatis**: AI akan menganalisis gambar dan menciptakan puisi yang unik.
    3.  **Narasi Suara**: Puisi tersebut akan dibacakan dengan suara yang ekspresif.
- **Interaksi Suara (ASR)**: Berbicara langsung ke aplikasi dan saksikan ucapan Anda diubah menjadi teks secara *real-time*.
- **Autentikasi & Riwayat**: Daftar untuk menyimpan riwayat percakapan dan mengakses fitur lanjutan.

## 🚀 Tumpukan Teknologi (Tech Stack)

Arsitektur SIGANTENG dibangun di atas teknologi modern yang andal dan skalabel, dengan fokus khusus pada model AI yang dioptimalkan untuk Bahasa Indonesia.

| Kategori | Teknologi / Model AI | Keterangan |
| :--- | :--- | :--- |
| **Frontend** | [Next.js](https://nextjs.org/), TypeScript, Tailwind CSS | Antarmuka pengguna yang modern dan responsif. |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/), Python | API berperforma tinggi untuk orkestrasi AI. |
| **Database** | [Neon](https://neon.tech/) (PostgreSQL) | Database *serverless* yang skalabel. |
| **Autentikasi** | [Clerk](https://clerk.com/) | Manajemen pengguna dan sesi yang aman. |
| **Penyimpanan** | [Cloudinary](https://cloudinary.com/) | Penyimpanan dan pengiriman aset media. |
| | | |
| **Visi (CV)** | `Salesforce/blip-image-captioning-base` | Menganalisis dan memberi deskripsi pada gambar. |
| **NLP (Teks)** | `cahya/gpt2-small-indonesian` | Menghasilkan puisi dalam Bahasa Indonesia. |
| **Analisis Sentimen**| `indobenchmark/indobert-base-p2` | Memahami sentimen dari teks berbahasa Indonesia. |
| **ASR (Suara → Teks)**| `openai/whisper-base` | Mengubah ucapan menjadi teks. |
| **TTS (Teks → Suara)**| `facebook/mms-tts-ind` | Menghasilkan narasi suara dalam Bahasa Indonesia. |
| **Embeddings (KB)**| `all-MiniLM-L6-v2` | *[Masa Depan]* Untuk fitur pencarian semantik. |

## 🛠️ Memulai Proyek

Untuk menjalankan proyek ini secara lokal, ikuti langkah-langkah berikut.

### Prasyarat

- Node.js (v20 atau lebih baru)
- Python (v3.11 atau lebih baru)
- Akun di [Neon](https://neon.tech/), [Clerk](https://clerk.com/), dan [Cloudinary](https://cloudinary.com/).

### 1. Kloning Repositori

```bash
git clone https://github.com/username/siganteng.git
cd siganteng
```

### 2. Konfigurasi Environment

Proyek ini membutuhkan beberapa kunci API dan kredensial.

1.  Salin file `.env.example` di root direktori dan di dalam `backend/` menjadi `.env`.
    ```bash
    cp .env.example .env
    cp backend/.env.example backend/.env
    ```
2.  Isi semua variabel yang diperlukan di kedua file `.env` dengan kredensial yang Anda dapatkan dari Neon, Clerk, dan Cloudinary.

### 3. Instalasi & Menjalankan

Buka dua terminal terpisah untuk Frontend dan Backend.

**Terminal 1: Frontend**
```bash
# Arahkan ke direktori frontend
cd frontend

# Install dependensi
npm install

# Jalankan server pengembangan
npm run dev
```
Frontend akan berjalan di `http://localhost:3000`.

**Terminal 2: Backend**
```bash
# Arahkan ke direktori backend
cd backend

# (Opsional, disarankan) Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows

# Install dependensi
pip install -r requirements.txt

# Jalankan server pengembangan
uvicorn app.main:app --reload
```
Backend akan berjalan di `http://localhost:8000`. Anda bisa mengakses dokumentasi API di `http://localhost:8000/docs`.

## 📂 Struktur Proyek

Proyek ini memiliki struktur monorepo sederhana dengan dua direktori utama: `frontend` dan `backend`.

- **`/frontend`**: Aplikasi Next.js yang menangani semua antarmuka pengguna (UI) dan interaksi sisi klien.
- **`/backend`**: API FastAPI yang menyediakan layanan AI, mengelola data, dan berinteraksi dengan database.
- **Dokumentasi**: File seperti `system_design.md` dan `architect.plantuml` menjelaskan arsitektur dan alur sistem secara mendalam.

Lihat `file_tree.md` untuk rincian struktur file yang lebih lengkap.