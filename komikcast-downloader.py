import os
import time
import requests
import img2pdf
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# Headers agar tidak terdeteksi sebagai bot
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def download_image(url, save_path, retries=5):
    """ Mengunduh gambar dengan retry hingga 5x jika gagal """
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
        time.sleep(2)  # jeda sebelum mencoba ulang

    print(f"[FAIL] Gagal mengunduh {url} setelah {retries} percobaan.")
    return False

def compress_image(input_path, output_path, quality=30):
    """ Mengompresi gambar untuk menghemat ukuran """
    print(f"[COMPRESS] Mengompresi: {input_path} -> {output_path}")
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality)
    os.remove(input_path)
    print(f"[COMPRESS] Disimpan: {output_path}")

def create_pdf(image_folder, output_pdf):
    """ Membuat PDF dari semua gambar dalam folder """
    print(f"[PDF] Membuat PDF dari folder: {image_folder}")
    images = [os.path.join(image_folder, img) for img in sorted(os.listdir(image_folder)) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not images:
        print(f"[ERROR] Tidak ada gambar ditemukan. PDF tidak dibuat!")
        return
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(images))
    print(f"[PDF] PDF berhasil dibuat: {output_pdf}")

def scrape_and_save_chapter(comic_slug, chapter_num, output_folder):
    # Handle chapter numbers with decimal points (like 39.1 becomes 39-1)
    formatted_chapter = str(chapter_num).replace('.', '-')
    url = f"https://komikcast02.com/chapter/{comic_slug}-chapter-{formatted_chapter}/"
    print(f"\n[CHAPTER {chapter_num}] Mengakses: {url}")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    print(f"[CHAPTER {chapter_num}] Mengekstrak gambar...")
    images = driver.find_elements(By.TAG_NAME, "img")
    img_urls = [img.get_attribute("src") for img in images if "alignnone" in (img.get_attribute("class") or "")]

    driver.quit()

    if not img_urls:
        print(f"[WARNING] Tidak ada gambar ditemukan di {url}.")
        return
    
    chapter_folder = os.path.join(output_folder, f"chapter_{formatted_chapter.replace('-', '_')}")
    os.makedirs(chapter_folder, exist_ok=True)
    
    for idx, img_url in enumerate(img_urls):
        original_img = os.path.join(chapter_folder, f"{idx+1}.jpg")
        compressed_img = os.path.join(chapter_folder, f"compressed_{idx+1}.jpg")
        
        if download_image(img_url, original_img):
            compress_image(original_img, compressed_img, quality=30)
        else:
            print(f"[SKIP] Melewati gambar ke-{idx+1} karena gagal diunduh.")

    pdf_output = os.path.join(output_folder, f"{comic_slug}-Chapter-{formatted_chapter}.pdf")
    create_pdf(chapter_folder, pdf_output)

def main():
    comic_slug = input("Masukkan judul komik (misal: owari-no-seraph): ").strip()
    
    # Ask user for download mode
    print("\nPilih mode download:")
    print("1. Download range chapter (misal: chapter 10 sampai 20)")
    print("2. Download chapter tertentu (pisahkan dengan spasi, misal: 39.1 50.2 60)")
    choice = input("Masukkan pilihan (1/2): ").strip()
    
    output_folder = f"{comic_slug}_PDFs"
    os.makedirs(output_folder, exist_ok=True)

    if choice == '1':
        # Range mode
        start_chapter = float(input("Masukkan chapter awal: ").strip())
        end_chapter = float(input("Masukkan chapter akhir: ").strip())
        
        # Handle integer and float chapters
        if start_chapter.is_integer() and end_chapter.is_integer():
            for chapter in range(int(start_chapter), int(end_chapter) + 1):
                scrape_and_save_chapter(comic_slug, chapter, output_folder)
        else:
            current = start_chapter
            while current <= end_chapter:
                scrape_and_save_chapter(comic_slug, current, output_folder)
                current = round(current + 0.1, 1)  # Increment by 0.1 for decimal chapters
    
    elif choice == '2':
        # Specific chapters mode
        chapters_input = input("Masukkan chapter yang ingin didownload (pisahkan dengan spasi, misal: 39.1 50.2 60): ").strip()
        chapters = chapters_input.split()
        
        for chapter in chapters:
            try:
                chapter_num = float(chapter)
                scrape_and_save_chapter(comic_slug, chapter_num, output_folder)
            except ValueError:
                print(f"[ERROR] '{chapter}' bukan format chapter yang valid. Dilewati.")
    
    else:
        print("[ERROR] Pilihan tidak valid. Harap pilih 1 atau 2.")
        return

    print("\nScraping selesai!")

if __name__ == "__main__":
    main()
