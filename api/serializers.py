from rest_framework import serializers
from .models import Player, Game, GameComment

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'email', 'password', 'elo', 'rank', 'country', 'wins', 'losses', 'draws']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        player = Player.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            elo=validated_data.get('elo', 800),
            rank=validated_data.get('rank', 'pawn')
        )
        return player

class GameCommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='player.username')
    class Meta:
        model = GameComment
        fields = ['id', 'username', 'content', 'created_at']

class GameSerializer(serializers.ModelSerializer):
    white_username = serializers.ReadOnlyField(source='white_player.username')
    black_username = serializers.ReadOnlyField(source='black_player.username')
    comments = GameCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = '__all__'
