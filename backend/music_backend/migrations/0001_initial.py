# Generated by Django 5.2.1 on 2025-05-26 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_type', models.CharField(choices=[('CNN', 'CNN'), ('DNN', 'DNN')], max_length=5, verbose_name='Model Tipi')),
                ('input_type', models.CharField(choices=[('FILE', 'Dosya'), ('YOUTUBE', 'YouTube')], max_length=10, verbose_name='Giriş Tipi')),
                ('input_path', models.CharField(max_length=255, verbose_name='Dosya Yolu')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
                ('youtube_url', models.URLField(blank=True, max_length=500, null=True)),
                ('original_filename', models.CharField(max_length=255, null=True)),
                ('blues', models.FloatField(verbose_name='Blues Olasılığı')),
                ('classical', models.FloatField(verbose_name='Klasik Olasılığı')),
                ('country', models.FloatField(verbose_name='Country Olasılığı')),
                ('disco', models.FloatField(verbose_name='Disco Olasılığı')),
                ('hiphop', models.FloatField(verbose_name='Hiphop Olasılığı')),
                ('jazz', models.FloatField(verbose_name='Jazz Olasılığı')),
                ('metal', models.FloatField(verbose_name='Metal Olasılığı')),
                ('pop', models.FloatField(verbose_name='Pop Olasılığı')),
                ('reggae', models.FloatField(verbose_name='Reggae Olasılığı')),
                ('rock', models.FloatField(verbose_name='Rock Olasılığı')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı')),
            ],
            options={
                'verbose_name': 'Tahmin Geçmişi',
                'verbose_name_plural': 'Tahmin Geçmişi',
            },
        ),
    ]
