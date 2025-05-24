from django.db import models
from django.conf import settings

class UserAudio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_file = models.FileField(
        upload_to='uploads/original/%Y/%m/%d/',
        null=True,
        blank=True
    )
    youtube_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    converted_wav = models.FileField(
        upload_to='uploads/converted/%Y/%m/%d/'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    prediction = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"