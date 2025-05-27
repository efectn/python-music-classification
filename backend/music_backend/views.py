# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.core.files import File
from django.db import models
import os
import librosa
import numpy as np
import tensorflow as tf
from .models import PredictionHistory
from music_backend.utils.audio_processor import (
    handle_uploaded_file,
    convert_to_wav,
    download_youtube_audio,
    load_and_pad_audio,
    extract_mfcc_segments
)

model_cnn = tf.keras.models.load_model(f'{settings.MODELS_DIR}/model_cnn.h5')
model_dnn = tf.keras.models.load_model(f'{settings.MODELS_DIR}/model_dnn.h5')
model_lstm = tf.keras.models.load_model(f'{settings.MODELS_DIR}/model_lstm.h5')
model_cnn_rnn = tf.keras.models.load_model(f'{settings.MODELS_DIR}/model_cnn2.h5')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı Adı',
            'id': 'login-username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre',
            'id': 'login-password',
        })
    )

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'index.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('home')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')  # URL pattern name’in 'login' olduğuna dikkat et
    model_type = request.session.get('model_type', 'CNN')
    return render(request, 'upload.html', {'model_type': model_type})

@login_required
def analyze_music(request):
    if request.method == 'POST':
        try:
            model_type = request.session.get('model_type', 'CNN')
            input_type = request.POST.get('input_type')
            youtube_url = request.POST.get('youtube_url', '')
            title = ""
            temp_path = None
            
            if input_type == 'FILE':
                uploaded_file = request.FILES['audio_file']
                temp_path = handle_uploaded_file(uploaded_file)
                final_path = convert_to_wav(temp_path)
            elif input_type == 'YOUTUBE':
                final_path, title = download_youtube_audio(youtube_url)
            else:
                return JsonResponse({'error': 'Geçersiz girdi tipi'}, status=400)

            segments, sr = load_and_pad_audio(final_path, sample_rate=22500, target_duration=30)

            model = model_cnn
            if model_type == 'CNN':
                model = model_cnn
            elif model_type == 'DNN':
                model = model_dnn
            elif model_type == 'LSTM':
                model = model_lstm
            elif model_type == 'CNNRNN':
                model = model_cnn_rnn

            all_mfcc_segments = []

            for segment in segments:
                mfcc_segments = extract_mfcc_segments(segment, sr)
                all_mfcc_segments.extend(mfcc_segments)

            segment_predictions = []
            for mfcc_segment in all_mfcc_segments:
                X = mfcc_segment[np.newaxis, ...]
                if model_type == 'CNN':
                    X = X[..., np.newaxis]

                prediction = model.predict(X)
                segment_predictions.append(prediction[0])

            average_prediction = np.mean(segment_predictions, axis=0)

            genres = ['blues', 'classical', 'country', 'disco', 'hiphop',
                      'jazz', 'metal', 'pop', 'reggae', 'rock']

            results = {genre: float(average_prediction[i]) * 100 for i, genre in enumerate(genres)}

            filename=os.path.basename(final_path)
            if title == "":
                title = filename

            PredictionHistory.objects.create(
                user=request.user,
                model_type=model_type,
                input_type=input_type,
                input_path=title,
                youtube_url=youtube_url if input_type == 'YOUTUBE' else '',
                **results
            )
            
            # Remove temporary file if it exists
            try:
                if os.path.exists(final_path):
                    os.remove(final_path)
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
            finally:
                pass
            
            return JsonResponse(results)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Sadece POST isteği kabul edilir'}, status=400)

@login_required
def preferences(request):
    if request.method == "POST":
        model_type = request.POST.get("model_type", "CNN")
        request.session["model_type"] = model_type
        return redirect("preferences")
    return render(request, "preferences.html")

@login_required
def analysis(request):
    # Fetch the user's prediction history, most recent first
    history = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'analysis.html', {'history': history})

@login_required
def stats(request):
    history = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')
    # Aggregate average probabilities for each genre
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    genre_averages = {}
    for genre in genres:
        avg = history.aggregate(avg=models.Avg(genre))[f'avg'] or 0
        genre_averages[genre] = round(avg, 1)
    return render(request, 'stats.html', {
        'history': history,
        'genre_averages': genre_averages,
    })
    
def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)