# Struktur File Proyek SIGANTENG

Berikut adalah gambaran struktur direktori dan file utama dalam proyek SIGANTENG.

```
SIGANTENG/
├── .env.example            # Contoh variabel lingkungan untuk root
├── .gitignore              # File dan folder yang diabaikan oleh Git
├── architect.plantuml      # Diagram arsitektur sistem
├── file_tree.md            # Dokumen ini
├── README.md               # Dokumentasi utama proyek
├── system_design.md        # Penjelasan desain sistem
├── ui_navigation.plantuml  # Diagram alur navigasi UI
│
├── backend/                # Direktori untuk aplikasi Backend (FastAPI)
│   ├── .env.example        # Contoh variabel lingkungan untuk backend
│   ├── Dockerfile          # Konfigurasi Docker untuk backend
│   ├── main.py             # Titik masuk utama aplikasi FastAPI
│   ├── README.md           # Dokumentasi khusus backend
│   ├── requirements.txt    # Dependensi Python
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/            # Modul untuk endpoint API
│   │   │   └── v1/
│   │   ├── core/           # Konfigurasi inti (env, dll)
│   │   ├── models/         # Skema data (Pydantic, SQLAlchemy)
│   │   ├── services/       # Logika bisnis (orkestrasi AI, dll)
│   │   └── utils/          # Fungsi bantuan
│   │
│   ├── data/               # (Opsional) Direktori untuk data lokal
│   │   └── .gitkeep
│   └── tests/              # Tes untuk backend
│       └── .gitkeep
│
└── frontend/               # Direktori untuk aplikasi Frontend (Next.js)
    ├── next.config.js
    ├── package.json        # Dependensi Node.js
    ├── postcss.config.js
    ├── tailwind.config.ts
    ├── tsconfig.json
    │
    ├── public/             # Aset statis (gambar, ikon)
    │   └── favicon.ico
    │
    └── src/
        ├── app/            # App Router Next.js
        │   ├── layout.tsx  # Layout utama
        │   ├── page.tsx    # Halaman utama (landing page)
        │   ├── api/        # Rute API Next.js (misal: untuk auth)
        │   └── chat/       # Halaman untuk antarmuka chat
        │       └── page.tsx
        │
        ├── components/     # Komponen React yang dapat digunakan kembali
        │   ├── AudioRecorder.tsx
        │   ├── ChatInput.tsx
        │   └── ...
        │
        ├── lib/            # Fungsi bantuan dan utilitas frontend
        ├── styles/         # File CSS global
        └── types/          # Definisi tipe TypeScript
```

## Deskripsi Direktori Utama

-   **`backend/`**: Berisi semua kode sisi server. Dibangun dengan FastAPI, direktori ini menangani logika berat seperti pemrosesan AI, interaksi database, dan menyediakan data untuk frontend.
-   **`frontend/`**: Berisi semua kode sisi klien. Dibangun dengan Next.js, direktori ini bertanggung jawab untuk merender antarmuka pengguna yang dilihat dan diinteraksikan oleh pengguna di browser mereka.
-   **File Root (`.md`, `.plantuml`)**: Berisi dokumentasi tingkat tinggi yang memberikan gambaran umum tentang proyek, arsitektur, dan desainnya. Ini adalah titik awal yang baik untuk memahami proyek secara keseluruhan.
