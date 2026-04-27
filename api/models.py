from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    RANKS = [
        ('pawn', 'Pawn'),
        ('knight', 'Knight'),
        ('rook', 'Rook'),
        ('king', 'King'),
        ('master', 'Master'),
        ('grandmaster', 'Grandmaster'),
    ]
    
    elo = models.IntegerField(default=800)
    rank = models.CharField(max_length=20, choices=RANKS, default='pawn')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Stats
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    best_elo = models.IntegerField(default=800)
    
    # Location (For African regional features)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.elo})"

class Game(models.Model):
    GAME_TYPES = [
        ('bullet', 'Bullet'),
        ('blitz', 'Blitz'),
        ('rapid', 'Rapid'),
        ('classical', 'Classical'),
    ]
    
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('draw', 'Draw'),
        ('aborted', 'Aborted'),
    ]

    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_white')
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_black')
    
    game_type = models.CharField(max_length=20, choices=GAME_TYPES, default='rapid')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    
    # Store moves in PGN format
    pgn = models.TextField(blank=True)
    current_fen = models.TextField(default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    
    # Record ELO change
    white_elo_change = models.IntegerField(null=True, blank=True)
    black_elo_change = models.IntegerField(null=True, blank=True)
    
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Game {self.id}: {self.white_player} vs {self.black_player}"

class GameComment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.username}: {self.content[:20]}"

class Puzzle(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    fen = models.TextField() # The board position
    solution = models.CharField(max_length=20) # The correct move (e.g., 'e2e4')
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    elo_rating = models.IntegerField(default=1200)
    
    def __str__(self):
        return f"Puzzle {self.id} ({self.difficulty})"

class Achievement(models.Model):
    # ... rest of the file
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50) # FontAwesome or Lucide icon name
    players = models.ManyToManyField(Player, related_name='achievements', blank=True)

    def __str__(self):
        return self.name
