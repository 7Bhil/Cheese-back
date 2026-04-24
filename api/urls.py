from django.urls import path
from .views import RegisterPlayerView, LoginView

urlpatterns = [
    path('register/', RegisterPlayerView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
