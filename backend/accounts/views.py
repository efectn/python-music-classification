from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import joblib

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('home')

def home(request):
    return render(request, 'accounts/home.html')


@login_required
def predict_genre(request):
    if request.method == 'POST':
        try:
            # Model yükleme
            model_path = os.path.join(settings.MODELS_DIR, 'music_genre_model.pkl')
            model = joblib.load(model_path)

            # Dosya işleme kısmı (Örnek - gerçek implementasyon modelinize bağlı)
            uploaded_file = request.FILES['music_file']

            # Burada dosya işleme ve tahmin kodlarınız olacak
            # Örnek tahmin:
            prediction = model.predict([uploaded_file.read()])

            # Sonucu session'a kaydet
            request.session['latest_prediction'] = prediction[0]
            return redirect('home')

        except Exception as e:
            # Hata yönetimi
            print(f"Hata oluştu: {str(e)}")
            return render(request, 'accounts/predict.html', {'error': str(e)})

    return render(request, 'accounts/predict.html')