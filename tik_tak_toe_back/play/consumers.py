import json
from channels.generic.websocket import AsyncWebsocketConsumer
from play.services.play_factory import create_play


class SearchPlay(AsyncWebsocketConsumer):
    search_users = set(tuple())

    async def connect(self):
        self.user = self.scope["user"]
        self.type_play = self.scope['url_route']['kwargs']['type_play']
        self.search_users.add((self.user, self.type_play))
        await self.channel_layer.group_add(self.user.username, self.channel_name)
        await self.accept()
        await self.check_searcher()

    async def disconnect(self, close_code):
        try:
            self.search_users.remove(self.user)
        except KeyError:
            pass
        await self.channel_layer.group_discard(self.user.username, self.channel_name)

    async def check_searcher(self):
        matching_users = list(filter(lambda x: x[-1] == self.type_play, self.search_users))
        if len(matching_users) >= 2:
            user_to_connect = matching_users[:2]
            self.search_users.difference_update(user_to_connect)
            await self.connect_users(user_to_connect)

    async def connect_users(self, users):
        # We takes {(<User: nikakoy_>, '3x3'), (<User: Vera>, '3x3')} as data for connecting
        play_hash_code = await create_play(users, self.type_play)
        if play_hash_code:
            for user in users:
                try:
                    await self.send_user_message(user[0].username, {'msg': 'successful',
                                                                    'play_hash_code': play_hash_code})
                except ConnectionResetError:
                    await self.disconnect_connected_user(user[0])
                    break
                except TimeoutError as e:
                    await self.send_user_message(user[0].username, {'error': e.strerror})

    async def disconnect_connected_user(self, user):
        self.search_users.remove(user)
        await self.channel_layer.group_discard(user.username, self.channel_name)

    async def send_user_message(self, group_name: str, message: dict):
        await self.channel_layer.group_send(
            group_name,
            {
                'type': 'send_message',
                'data': message,
            }
        )

    async def send_message(self, event):
        message = event['data']
        await self.send(text_data=json.dumps(message))



