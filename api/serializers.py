from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'email', 'password', 'elo', 'rank', 'country']
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
