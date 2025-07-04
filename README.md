# 📚 Scrape-Komikcast

**Scrape-Komikcast** adalah koleksi skrip Python untuk mengunduh konten dari situs-situs seperti **Komikcast**, **Komiku**, dan media sosial (melalui `social-dl.py` dan `fb_downloader.py`).

---

## 🛠️ Instalasi

### Prasyarat

Pastikan Python sudah terinstal. Lalu, instal dependensi berikut:

```bash
pip install selenium img2pdf requests==1.26 yt-dlp bs4
```

---

## 📄 Daftar File

* `komikcast.py` — Scraper utama untuk situs Komikcast
* `komikcast-downloader.py` — Automasi unduhan komik dari Komikcast
* `komiku.py` — Untuk mengunduh dari Komiku
* `social-dl.py` — Downloader media sosial
* `fb_downloader.py` — Fokus pada pengunduhan video Facebook

---

## 🚀 Menjalankan Skrip

Contoh penggunaan untuk mengunduh dari Komikcast:

```bash
python komikcast.py
```

Silakan sesuaikan argumen atau URL di dalam skrip sesuai target.

---

## ⚠️ Catatan Penting

* Beberapa fitur mungkin memerlukan **WebDriver** (seperti ChromeDriver) jika menggunakan Selenium.
* Untuk `yt-dlp` pastikan file biner tersedia atau instal via pip:

```bash
pip install -U yt-dlp
```

---

## 📜 Lisensi

Lisensi: Tidak disebutkan secara eksplisit, silakan hubungi pengelola repo untuk informasi lebih lanjut.

---

## 👤 Pengembang

Project ini dibuat oleh [SecretDiscorder](https://github.com/SecretDiscorder).

Gunakan dengan bijak dan hormati hak cipta situs target. 🙏
