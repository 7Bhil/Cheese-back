from django.urls import path
from .views import (
    RegisterPlayerView, LoginView, RecordGameView, ProfileView, 
    LeaderboardView, PuzzleListView, OngoingGamesView, GameDetailView, AddCommentView,
    CreateDuelView
)

urlpatterns = [
    path('register/', RegisterPlayerView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('record-game/', RecordGameView.as_view(), name='record_game'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('puzzles/', PuzzleListView.as_view(), name='puzzles'),
    path('ongoing-games/', OngoingGamesView.as_view(), name='ongoing_games'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('game/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('create-duel/', CreateDuelView.as_view(), name='create_duel'),
]
