# utils/audio_processor.py
import os
import subprocess
import numpy as np
import math
import librosa
import yt_dlp
from django.conf import settings
import uuid

def load_and_pad_audio(audio_file, sample_rate=22500, target_duration=30):
    signal, sr = librosa.load(audio_file, sr=sample_rate)
    total_duration = librosa.get_duration(y=signal, sr=sr)

    target_length = sample_rate * target_duration  # örn. 30 saniye
    full_segments = int(np.ceil(total_duration / target_duration))

    padded_signal = []

    for i in range(full_segments):
        start = int(i * target_length)
        end = int((i + 1) * target_length)
        segment = signal[start:end]

        if len(segment) < target_length:
            # Padding with zeros to reach 30s
            padding = np.zeros(int(target_length - len(segment)))
            segment = np.concatenate((segment, padding))

        padded_signal.append(segment)

    return padded_signal, sr

def extract_mfcc_segments(segment, sr, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=10):
    samples_per_segment = int(len(segment) / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

    mfccs = []
    for d in range(num_segments):
        start = samples_per_segment * d
        finish = start + samples_per_segment

        mfcc = librosa.feature.mfcc(
            y=segment[start:finish],
            sr=sr,
            n_fft=n_fft,
            hop_length=hop_length,
            n_mfcc=num_mfcc
        )
        mfcc = mfcc.T
        if mfcc.shape[0] == num_mfcc_vectors_per_segment:
            mfccs.append(mfcc)

    return np.array(mfccs)


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
        '-y',
        '-i', input_path,
        '-acodec', 'pcm_s16le',
        '-ar', '22500',
        output_path
    ]
    subprocess.run(command, check=True)
    return output_path


def download_youtube_audio(url, output_dir='youtube_downloads'):
    # Çıktı dizinini oluştur
    os.makedirs(os.path.join(settings.MEDIA_ROOT, output_dir), exist_ok=True)

    # Rastgele dosya adı oluştur
    random_filename = str(uuid.uuid4())

    ydl_opts = {
        'playlist_items': '1',
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(settings.MEDIA_ROOT, output_dir, f'{random_filename}.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get('title')
        downloaded_path = os.path.join(settings.MEDIA_ROOT, output_dir, f"{random_filename}.wav")

    return downloaded_path, title
