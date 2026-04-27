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
        message_type = text_data_json.get('type', 'game_move')
        
        if message_type == 'game_move':
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
        elif message_type == 'game_comment':
            comment = text_data_json.get('comment')
            username = text_data_json.get('username')
            
            await self.channel_layer.group_send(
                self.game_group_name,
                {
                    'type': 'game_comment',
                    'comment': comment,
                    'username': username
                }
            )

    # Receive message from game group
    async def game_move(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_move',
            'move': event['move'],
            'fen': event['fen'],
            'sender': event['sender']
        }))

    async def game_comment(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_comment',
            'comment': event['comment'],
            'username': event['username']
        }))
