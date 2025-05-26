from django.contrib import admin
from .models import PredictionHistory
from django.contrib.auth.models import User

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'model_type', 'input_type', 'top_genre', 'created_at')
    list_filter = ('model_type', 'input_type')
    search_fields = ('user__username', 'input_path')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def top_genre(self, obj):
        genre_scores = {
            'blues': obj.blues,
            'classical': obj.classical,
            'country': obj.country,
            'disco': obj.disco,
            'hiphop': obj.hiphop,
            'jazz': obj.jazz,
            'metal': obj.metal,
            'pop': obj.pop,
            'reggae': obj.reggae,
            'rock': obj.rock,
        }
        top = max(genre_scores, key=genre_scores.get)
        return f"{top} ({genre_scores[top]:.1f}%)"

    top_genre.short_description = "En Yüksek Tür"
