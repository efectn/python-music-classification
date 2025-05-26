# utils/audio_processor.py
import os
import subprocess
import yt_dlp
from django.conf import settings


def handle_uploaded_file(uploaded_file, temp_dir='temp'):
    """Kullanıcıdan yüklenen dosyayı geçici olarak kaydeder."""
    os.makedirs(os.path.join(settings.MEDIA_ROOT, temp_dir), exist_ok=True)
    temp_path = os.path.join(settings.MEDIA_ROOT, temp_dir, uploaded_file.name)

    with open(temp_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return temp_path


def convert_to_wav(input_path, output_dir='converted'):
    """FFmpeg ile WAV formatına dönüştürür."""
    os.makedirs(os.path.join(settings.MEDIA_ROOT, output_dir), exist_ok=True)
    output_filename = os.path.basename(input_path).split('.')[0] + '.wav'
    output_path = os.path.join(settings.MEDIA_ROOT, output_dir, output_filename)

    command = [
        'ffmpeg',
        '-i', input_path,
        '-acodec', 'pcm_s16le',
        '-ar', '22500',
        output_path
    ]
    subprocess.run(command, check=True)
    return output_path


def download_youtube_audio(url, output_dir='youtube_downloads'):
    """YouTube'dan sesi indirip WAV'a çevirir."""
    os.makedirs(os.path.join(settings.MEDIA_ROOT, output_dir), exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(settings.MEDIA_ROOT, output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_path = ydl.prepare_filename(info).replace('.webm', '.wav')

    return downloaded_path