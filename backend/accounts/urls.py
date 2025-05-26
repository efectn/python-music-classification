from django.urls import path
from . import views

app_name = ''
handler404 = 'music_backend.views.custom_404_view'

urlpatterns = [
    # Path for the home page (upload page)
    # This corresponds to LOGIN_REDIRECT_URL = '/' if accounts.urls is included at the project root.
    path('', views.home, name='home'),

    # Path for user registration (signup)
    path('signup/', views.signup, name='register'),

    # Path for user login
    path('login/', views.user_login, name='login'),

    # Path for user logout
    path('logout/', views.user_logout, name='logout'),

    # Path for the preferences page
    path('preferences/', views.preferences, name='preferences'),

    # Path for the statistics page
    path('stats/', views.stats, name='stats'),

    # Path for the analysis page (the page itself, not the AJAX endpoint)
    path('analysis-page/', views.analysis, name='analysis'),

    # Path for the music analysis AJAX endpoint
    path('analyze-music/', views.analyze_music, name='analyze_music'),

    # Path for the 'Müzik Tara' / 'Upload' link in navigation, which points to the home/upload page
    path('upload/', views.home, name='upload'),
    
    # pathfor 404
    path('404/', views.custom_404_view, name='custom_404_view'),
]