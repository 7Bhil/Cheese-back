from rest_framework import status, generics, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import Player, Game, Puzzle, GameComment, AILearning
from .serializers import PlayerSerializer, GameSerializer, PuzzleSerializer
import json

# Simple ELO Delta
K_FACTOR = 32

def calculate_elo(rating_w, rating_b, score_w):
    expected_w = 1 / (1 + 10 ** ((rating_b - rating_w) / 400))
    new_rating_w = rating_w + K_FACTOR * (score_w - expected_w)
    return round(new_rating_w)

class RegisterPlayerView(generics.CreateAPIView):
    queryset = Player.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PlayerSerializer

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        login_input = request.data.get('username')
        password = request.data.get('password')
        try:
            user_obj = Player.objects.get(Q(username=login_input) | Q(email=login_input))
            username = user_obj.username
        except Player.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(username=username, password=password)
        if user:
            serializer = PlayerSerializer(user)
            return Response({'user': serializer.data, 'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

class RecordGameView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        game_id = request.data.get('game_id')
        white_id = request.data.get('white_player')
        black_id = request.data.get('black_player')
        winner_id = request.data.get('winner')
        status_game = request.data.get('status')
        pgn = request.data.get('pgn')
        fen = request.data.get('fen')

        if game_id:
            game = Game.objects.get(id=game_id)
            game.status = status_game
            game.winner_id = winner_id
            game.pgn = pgn
            game.current_fen = fen
            game.save()
            
            if status_game == 'completed' or status_game == 'draw':
                # Update ELO only on completion
                white = game.white_player
                black = game.black_player
                score_w = 0.5
                if winner_id == str(white.id): score_w = 1
                elif winner_id == str(black.id): score_w = 0
                
                # AI Learning: If AI (ID 1) is Black and lost
                if black.id == 1 and score_w == 1:
                    AILearning.objects.get_or_create(
                        fen=fen,
                        defaults={'last_game': game}
                    )
                
                new_elo_w = calculate_elo(white.elo, black.elo, score_w)
                new_elo_b = calculate_elo(black.elo, white.elo, 1 - score_w)
                
                game.white_elo_change = new_elo_w - white.elo
                game.black_elo_change = new_elo_b - black.elo
                
                white.elo = new_elo_w
                black.elo = new_elo_b
                if score_w == 1:
                    white.wins += 1; black.losses += 1
                elif score_w == 0:
                    black.wins += 1; white.losses += 1
                else:
                    white.draws += 1; black.draws += 1
                white.save(); black.save(); game.save()

            return Response({'message': 'Game updated', 'game_id': game.id, 'white_elo': white.elo if status_game == 'completed' else None})

        # Create new game
        white = Player.objects.get(id=white_id)
        black = Player.objects.get(id=black_id)
        game = Game.objects.create(
            white_player=white,
            black_player=black,
            status='ongoing',
            pgn=pgn,
            current_fen=fen
        )
        return Response({'message': 'Game started', 'game_id': game.id}, status=status.HTTP_201_CREATED)

class OngoingGamesView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        games = Game.objects.filter(status='ongoing').order_by('-updated_at')[:10]
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

class GameDetailView(generics.RetrieveAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (AllowAny,)

class AddCommentView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
            content = request.data.get('content')
            if not content:
                return Response({'error': 'Comment is empty'}, status=400)
            from .models import GameComment
            comment = GameComment.objects.create(
                game=game,
                player=request.user,
                content=content
            )
            return Response({'message': 'Comment added'}, status=201)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=404)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = PlayerSerializer(user)
        games = Game.objects.filter(Q(white_player=user) | Q(black_player=user)).order_by('-created_at')[:10]
        games_serializer = GameSerializer(games, many=True)
        return Response({'user': serializer.data, 'recent_games': games_serializer.data}, status=status.HTTP_200_OK)

class LeaderboardView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        top_players = Player.objects.all().order_by('-elo')[:10]
        serializer = PlayerSerializer(top_players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateDuelView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        opponent_id = request.data.get('opponent_id')
        try:
            opponent = Player.objects.get(id=opponent_id)
            game = Game.objects.create(
                white_player=request.user,
                black_player=opponent,
                status='ongoing' # In a real pvp, it would be 'pending'
            )
            return Response({'game_id': game.id}, status=201)
        except Player.DoesNotExist:
            return Response({'error': 'Player not found'}, status=404)

class PuzzleListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        puzzles = Puzzle.objects.all().order_by('?')[:5] # Random puzzles
        serializer = PuzzleSerializer(puzzles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
