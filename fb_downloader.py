import yt_dlp

def download_facebook_video(fb_url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Tentukan nama file keluaran
        'format': 'best',  # Pilih kualitas video terbaik
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([fb_url])
        print("Video downloaded successfully.")
    except Exception as e:
        print(f"Failed to download the video: {str(e)}")

# Prompt the user to enter the Facebook video URL
fb_url = input("Enter the Facebook video URL: ")

# Download the video
download_facebook_video(fb_url)
