from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model
User = get_user_model()


# YENİ EKLENEN MODEL
class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    model_type = models.CharField(max_length=5, choices=[('CNN', 'CNN'), ('DNN', 'DNN')], verbose_name="Model Tipi")
    input_type = models.CharField(max_length=10, choices=[('FILE', 'Dosya'), ('YOUTUBE', 'YouTube')],
                                  verbose_name="Giriş Tipi")
    input_path = models.CharField(max_length=255, verbose_name="Dosya Yolu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    
    youtube_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    original_filename = models.CharField(max_length=255, null=True)

    # Tahmin Sonuçları
    blues = models.FloatField(verbose_name="Blues Olasılığı")
    classical = models.FloatField(verbose_name="Klasik Olasılığı")
    country = models.FloatField(verbose_name="Country Olasılığı")
    disco = models.FloatField(verbose_name="Disco Olasılığı")
    hiphop = models.FloatField(verbose_name="Hiphop Olasılığı")
    jazz = models.FloatField(verbose_name="Jazz Olasılığı")
    metal = models.FloatField(verbose_name="Metal Olasılığı")
    pop = models.FloatField(verbose_name="Pop Olasılığı")
    reggae = models.FloatField(verbose_name="Reggae Olasılığı")
    rock = models.FloatField(verbose_name="Rock Olasılığı")

    @property
    def top_genre(self):
        genre_scores = {
            'blues': self.blues,
            'classical': self.classical,
            'country': self.country,
            'disco': self.disco,
            'hiphop': self.hiphop,
            'jazz': self.jazz,
            'metal': self.metal,
            'pop': self.pop,
            'reggae': self.reggae,
            'rock': self.rock,
        }
        top = max(genre_scores, key=genre_scores.get)
        return f"{top.capitalize()} ({genre_scores[top]:.1f}%)"

    def __str__(self):
        # type: (PredictionHistory) -> str
        return f"{self.user.username} - {self.created_at}"  # .email yerine .username

    class Meta:
        verbose_name = "Tahmin Geçmişi"
        verbose_name_plural = "Tahmin Geçmişi"