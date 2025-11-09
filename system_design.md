# Dokumen Desain Sistem: SIGANTENG

Dokumen ini menguraikan arsitektur, alur interaksi, dan komponen teknis dari proyek **SIGANTENG**.

## 1. Visi & Tujuan

SIGANTENG adalah asisten AI multimodal yang bertujuan memberikan dua pengalaman pengguna utama:
1.  **"Magic Moment"**: Interaksi chat yang cepat dan mudah diakses tanpa perlu login, menciptakan kesan pertama yang positif.
2.  **"Wow Moment"**: Sebuah alur kreatif di mana AI mengubah gambar yang diunggah pengguna menjadi sebuah puisi, lalu membacakannya dengan suara yang ekspresif.

## 2. Arsitektur Sistem

Sistem ini menggunakan arsitektur terpisah (*decoupled*) yang memisahkan antara antarmuka pengguna (Frontend) dan logika bisnis (Backend).

![Arsitektur Tingkat Tinggi](architect.plantuml)

### Komponen Utama:

-   **Frontend (Next.js)**: Bertanggung jawab untuk semua yang dilihat dan diinteraksikan oleh pengguna. Ini adalah aplikasi web modern yang menghadirkan pengalaman pengguna yang cair dan responsif.
-   **Backend (FastAPI)**: Otak dari aplikasi. Menyediakan API untuk frontend, menjalankan model AI, dan berkomunikasi dengan database serta layanan pihak ketiga lainnya.
-   **Database (Neon PostgreSQL)**: Menyimpan data pengguna, riwayat percakapan, dan informasi terkait lainnya dalam format yang terstruktur dan skalabel.
-   **Autentikasi (Clerk)**: Mengelola pendaftaran, login, dan keamanan sesi pengguna dengan standar industri, memastikan data pengguna aman.
-   **Penyimpanan (Cloudinary)**: Menyimpan file media seperti gambar yang diunggah pengguna dan audio yang dihasilkan oleh AI, dengan pengiriman yang dioptimalkan secara global.

### Pemilihan Model AI

Pemilihan model AI adalah keputusan strategis yang bertujuan untuk menciptakan pengalaman yang relevan secara lokal dan kaya fitur. Setiap model dipilih berdasarkan performa, ukuran, dan kemampuannya untuk bekerja dengan baik dalam ekosistem Bahasa Indonesia.

-   **Visi - `Salesforce/blip-image-captioning-base`**: Model ini menawarkan keseimbangan yang baik antara kecepatan dan kualitas untuk menganalisis gambar dan memberikan deskripsi awal.
-   **Pembuatan Teks - `cahya/gpt2-small-indonesian`**: Kami secara spesifik memilih model GPT-2 yang telah dilatih untuk Bahasa Indonesia. Ini memastikan bahwa puisi yang dihasilkan tidak hanya benar secara tata bahasa, tetapi juga relevan secara budaya dan nuansa.
-   **Pemahaman Teks - `indobenchmark/indobert-base-p2`**: Untuk analisis sentimen atau pemahaman konteks, IndoBERT adalah pilihan yang superior karena dibangun dari korpus Bahasa Indonesia yang masif.
-   **Interaksi Suara (ASR & TTS)**:
    -   `openai/whisper-base` (ASR): Menambahkan dimensi interaksi baru dengan memungkinkan pengguna berbicara langsung ke aplikasi. Whisper dikenal karena akurasinya yang tinggi.
    -   `facebook/mms-tts-ind` (TTS): Model ini mampu menghasilkan suara dalam Bahasa Indonesia yang terdengar alami, yang sangat penting untuk pengalaman "Wow Moment" saat puisi dibacakan.
-   **Pencarian Masa Depan - `sentence-transformers/all-MiniLM-L6-v2`**: Model ini dipilih sebagai dasar untuk fitur *knowledge base* di masa depan karena kemampuannya yang efisien dalam membuat *embeddings* untuk pencarian semantik.

## 3. Alur Interaksi Pengguna

Alur pengguna dirancang agar intuitif dan memandu pengguna dari rasa penasaran hingga keterlibatan penuh.

![Alur Navigasi UI](ui_navigation.plantuml)

1.  **Kunjungan Pertama**: Pengguna tiba di halaman utama dan disambut dengan ajakan ("Coba Sekarang") untuk langsung mencoba **Magic Moment**.
2.  **Interaksi Awal**: Pengguna diarahkan ke halaman chat dan dapat langsung berinteraksi dengan AI.
3.  **Mencoba Wow Moment**: Pengguna mengunggah gambar, dan sistem akan memprosesnya menjadi puisi bersuara.
4.  **Konversi**: Setelah merasakan kemampuannya, pengguna akan ditawari secara halus untuk mendaftar agar dapat menyimpan riwayat percakapan mereka.
5.  **Pengguna Terdaftar**: Setelah login, pengguna dapat mengakses dasbor untuk melihat semua interaksi sebelumnya.

## 4. Struktur Data & API

### Model Data Utama

-   **User**: Informasi pengguna yang terdaftar.
-   **Conversation**: Kumpulan pesan dalam satu sesi interaksi.
-   **Message**: Pesan tunggal dari pengguna atau AI, bisa berisi teks, referensi gambar, atau referensi audio.

### Antarmuka API (Endpoints)

-   `POST /api/v1/ai/chat`: Mengirim dan menerima pesan chat sederhana.
-   `POST /api/v1/ai/wow-moment`: Memulai alur "Wow Moment" dengan mengirimkan gambar.
-   `GET /api/v1/conversations`: (Memerlukan Autentikasi) Mengambil riwayat percakapan pengguna.

## 5. Aspek Teknis & Keamanan

-   **Performa**: Model AI di-cache di memori backend setelah pemuatan pertama untuk mengurangi latensi pada permintaan berikutnya.
-   **Keamanan**: Autentikasi ditangani oleh Clerk menggunakan praktik standar industri. Semua komunikasi antara frontend dan backend dilakukan melalui HTTPS.
-   **Skalabilitas**: Arsitektur terpisah dan penggunaan layanan *serverless* (Neon, Cloudinary) memungkinkan setiap bagian dari sistem untuk diskalakan secara independen.
