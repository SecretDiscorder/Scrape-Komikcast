import os
import time
import re
import requests
import img2pdf
from PIL import Image, UnidentifiedImageError
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_image(url, save_path, retries=5):
    attempt = 0
    while attempt < retries:
        try:
            print(f"[DOWNLOAD] Mengunduh (Percobaan ke-{attempt + 1}): {url}")
            response = requests.get(url, stream=True, headers=HEADERS, timeout=10)
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"[DOWNLOAD] Disimpan: {save_path}")
                return True
            else:
                print(f"[ERROR] Status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Terjadi kesalahan: {e}")
        attempt += 1
        time.sleep(2)
    print(f"[FAIL] Gagal mengunduh {url} setelah {retries} percobaan.")
    return False

def compress_image(input_path, output_path, quality=30):
    try:
        print(f"[COMPRESS] Mengompresi: {input_path} -> {output_path}")
        with Image.open(input_path) as img:
            img = img.convert("RGB")
            img.save(output_path, "JPEG", quality=quality)
        os.remove(input_path)
        print(f"[COMPRESS] Disimpan: {output_path}")
    except (UnidentifiedImageError, OSError) as e:
        print(f"[ERROR] Gambar rusak atau tidak dikenali: {input_path} ({e})")
        if os.path.exists(input_path):
            os.remove(input_path)
        print(f"[SKIP] Gambar dilewati dan dihapus.")
from PIL import Image

import re

import os
import re
from PIL import Image
import img2pdf

def create_pdf(image_folder, output_pdf):
    print(f"[PDF] Membuat PDF dari folder: {image_folder}")

    # Fungsi untuk mengekstrak nomor urut dari nama file jika ada
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    # Mengambil semua gambar dengan ekstensi yang sesuai dan mengurutkannya secara alfabet
    image_paths = sorted([
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.lower().endswith((".jpg", ".jpeg", ".png"))
    ], key=lambda x: extract_number(os.path.basename(x)))

    # Pastikan gambar yang ditemukan tidak kosong
    if not image_paths:
        print("[ERROR] Tidak ada gambar valid ditemukan.")
        return

    # Daftar untuk menyimpan gambar yang akan dimasukkan ke dalam PDF
    images = []
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            img = img.convert("RGB")  # Mengonversi gambar ke mode RGB
            images.append(img)
        except Exception as e:
            print(f"[ERROR] Gagal membuka gambar {img_path}: {e}")

    # Membuat PDF
    try:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"[PDF] PDF berhasil dibuat: {output_pdf}")
    except Exception as e:
        print(f"[ERROR] Gagal membuat PDF: {e}")

# Tes fungsi dengan folder dan output PDF


def scrape_and_save_chapter(comic_slug, chapter_num, output_folder, convert_slug=False):
    if convert_slug:
        formatted_chapter = str(chapter_num).replace('.', '-')
    else:
        formatted_chapter = f"{int(chapter_num):02}" if isinstance(chapter_num, float) and chapter_num.is_integer() else str(chapter_num)

    url = f"https://komikcast02.com/chapter/{comic_slug}-chapter-{formatted_chapter}/"
    print(f"\n[CHAPTER {chapter_num}] Mengakses: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Gagal mengakses halaman: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    image_tags = soup.find_all("img", class_="alignnone")

    if not image_tags:
        print(f"[WARNING] Tidak ada gambar ditemukan di {url}.")
        return

    chapter_folder = os.path.join(output_folder, f"chapter_{formatted_chapter}")
    os.makedirs(chapter_folder, exist_ok=True)

    for idx, img_tag in enumerate(image_tags):
        img_url = img_tag.get("src")
        if not img_url:
            continue
        original_img = os.path.join(chapter_folder, f"{idx+1}.jpg")
        compressed_img = os.path.join(chapter_folder, f"compressed_{idx+1}.jpg")

        if download_image(img_url, original_img):
            compress_image(original_img, compressed_img)
        else:
            print(f"[SKIP] Melewati gambar ke-{idx+1} karena gagal diunduh.")

    pdf_output = os.path.join(output_folder, f"{comic_slug}-Chapter-{formatted_chapter}.pdf")
    create_pdf(chapter_folder, pdf_output)

def main():
    comic_slug = input("Masukkan judul komik (misal: owari-no-seraph): ").strip()

    print("\nPilih mode download:")
    print("1. Download range chapter (misal: chapter 10 sampai 20)")
    print("2. Download chapter tertentu (pisahkan dengan spasi, misal: 165.hq 165.2.lq 39.1)")
    choice = input("Masukkan pilihan (1/2): ").strip()

    output_folder = f"{comic_slug}_PDFs"
    os.makedirs(output_folder, exist_ok=True)

    if choice == '1':
        start_chapter = float(input("Masukkan chapter awal: ").strip())
        end_chapter = float(input("Masukkan chapter akhir: ").strip())

        current = start_chapter
        while current <= end_chapter:
            scrape_and_save_chapter(comic_slug, current, output_folder, convert_slug=False)
            current = round(current + 1 if current.is_integer() else 0.1, 1)

    elif choice == '2':
        chapters_input = input("Masukkan chapter yang ingin didownload (pisahkan dengan spasi): ").strip()
        chapters = chapters_input.split()

        for chapter in chapters:
            if re.match(r'^[\d\.a-zA-Z]+$', chapter):
                scrape_and_save_chapter(comic_slug, chapter.strip(), output_folder, convert_slug=True)
            else:
                print(f"[ERROR] Format tidak valid: '{chapter}', dilewati.")
    else:
        print("[ERROR] Pilihan tidak valid.")

if __name__ == "__main__":
    main()
