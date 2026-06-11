# Sharotta — Panduan Instalasi Django

## Struktur File

```
sharotta/                        ← app Django kamu
├── admin.py
├── models.py
├── views.py
├── urls.py
├── templates/
│   └── sharotta/
│       ├── base.html
│       └── home.html
└── static/
    └── css/
        └── style.css
```

---

## Langkah-langkah Instalasi

### 1. Tambahkan app ke settings.py

```python
INSTALLED_APPS = [
    ...
    'sharotta',
]
```

### 2. Konfigurasi TEMPLATES di settings.py

Pastikan `APP_DIRS: True` supaya Django bisa menemukan folder templates:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 3. Konfigurasi STATIC FILES di settings.py

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'sharotta' / 'static']

# Untuk upload thumbnail
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 4. Tambahkan URL di urls.py utama (project/urls.py)

```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sharotta.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 5. Install Pillow (untuk ImageField)

```bash
pip install Pillow
```

### 6. Jalankan migrasi

```bash
python manage.py makemigrations sharotta
python manage.py migrate
```

### 7. Buat superuser & isi data lewat Admin

```bash
python manage.py createsuperuser
python manage.py runserver
```

Buka `http://127.0.0.1:8000/admin/` untuk tambah:
- **Genre** — nama, slug, warna (pink/blue/green/purple/orange/teal/red)
- **Anime** — judul, genre, tipe (sub/dub/baru), rating, emoji, centang `is_populer`
- **Pengaturan** — teks pengumuman sidebar
- **Komentar** — opsional, bisa dari user

---

## Cara Kerja Data Dinamis

| Data di Template         | Sumbernya di views.py        |
|--------------------------|------------------------------|
| Baris genre filter       | `Genre.objects.all()`        |
| Grid "Baru Ditambahkan"  | `Anime` order by `-dibuat`   |
| Grid "Populer"           | `Anime` filter `is_populer`  |
| Top 5 sidebar            | `Anime` order by `-rating`   |
| Tag sidebar              | Sama dengan genre filter     |
| Komentar sidebar         | `Komentar` order by `-dibuat`|
| Pengumuman               | Model `Pengaturan`           |