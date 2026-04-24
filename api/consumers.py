import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'game_{self.game_id}'

        # Join game group
        await self.channel_layer.group_add(
            self.game_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave game group
        await self.channel_layer.group_discard(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        move = text_data_json.get('move')
        fen = text_data_json.get('fen')
        sender = text_data_json.get('sender')

        # Send message to game group
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                'type': 'game_move',
                'move': move,
                'fen': fen,
                'sender': sender
            }
        )

    # Receive message from game group
    async def game_move(self, event):
        move = event['move']
        fen = event['fen']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'move': move,
            'fen': fen,
            'sender': sender
        }))
