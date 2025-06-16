import yt_dlp
import os
import subprocess

def download_facebook_video(fb_url):
    # Menentukan folder Output
    output_folder = 'Output'
    os.makedirs(output_folder, exist_ok=True)  # Membuat folder jika belum ada
    
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Tentukan nama file dan folder output
        'format': 'bestvideo+bestaudio/best',  # Pilih kualitas terbaik video dan audio
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_url])
        print("Video downloaded successfully.")
    except Exception as e:
        print(f"Failed to download the video: {str(e)}")

def download_instagram_video(insta_url, cookies_file=None):
    # Menentukan folder Output
    output_folder = 'Output'
    os.makedirs(output_folder, exist_ok=True)  # Membuat folder jika belum ada
    
    subprocess.run(['yt-dlp', '--cookies', cookies_file, '-o', os.path.join(output_folder, '%(title)s.%(ext)s'), insta_url], capture_output=True, text=True)

def download_youtube_video(youtube_url, output_format='mp4'):
    # Menentukan folder Output
    output_folder = 'Output'
    os.makedirs(output_folder, exist_ok=True)  # Membuat folder jika belum ada
    
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Tentukan nama file dan folder output
        'format': f'bestvideo+bestaudio/best',  # Pilih kualitas terbaik video dan audio
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',  # Konversi video ke format yang diinginkan
            'preferedformat': output_format,  # Format yang dipilih (MP4 atau MP3)
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"Video downloaded successfully as {output_format.upper()}.")
    except Exception as e:
        print(f"Failed to download the YouTube video: {str(e)}")

def display_menu():
    print("\nPilih platform untuk mendownload video:")
    print("1. Facebook Video")
    print("2. Instagram Post/Video")
    print("3. Instagram Story")
    print("4. YouTube Video (MP4)")
    print("5. YouTube Audio (MP3)")
    print("6. Keluar")

def main():
    cookies_file = input("Masukkan path ke file cookies.txt (atau tekan Enter jika tidak menggunakan cookies): ")

    while True:
        display_menu()
        choice = input("Masukkan pilihan (1/2/3/4/5/6): ")

        if choice == '1':
            fb_url = input("Masukkan URL video Facebook: ")
            download_facebook_video(fb_url)
        elif choice == '2':
            insta_url = input("Masukkan URL video atau post Instagram: ")
            download_instagram_video(insta_url, cookies_file)
        elif choice == '3':
            insta_url = input("Masukkan URL Instagram Story: ")
            download_instagram_video(insta_url, cookies_file)
        elif choice == '4':
            youtube_url = input("Masukkan URL video YouTube: ")
            download_youtube_video(youtube_url, output_format='mp4')  # MP4 default
        elif choice == '5':
            youtube_url = input("Masukkan URL video YouTube: ")
            download_youtube_video(youtube_url, output_format='mp3')  # MP3 format
        elif choice == '6':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Program utama
if __name__ == "__main__":
    main()
