from django.urls import path
from .views import RegisterPlayerView

urlpatterns = [
    path('register/', RegisterPlayerView.as_view(), name='register'),
]
