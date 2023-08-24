import json
from channels.generic.websocket import AsyncWebsocketConsumer

from play.redis_services.redis_services import get_next_player, start_turn_timer
from play.services.play_factory import create_play
from play.services.play_services import is_player_in_game, get_user_from_play, check_board, upd_board, get_board


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
                                                                    'play_hash_code': play_hash_code,
                                                                    'type_play': self.type_play})
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


class PlayConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.play_hash_code = self.scope["url_route"]["kwargs"]["play_hash_code"]
        self.play_type = self.scope["url_route"]["kwargs"]["play_type"]
        self.play_name = "play_%s" % self.play_hash_code

        if not is_player_in_game:
            await self.close()

            await self.send(text_data=json.dumps({
                "type": 'INFO',
                "message": 'unsuccessfull',
                # will add exceptions
            }))

        await self.channel_layer.group_add(self.play_name, self.channel_name)
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": 'INFO',
            "message": 'successfully_connected_player',
        }))
        # channel__ = await self.channel_layer.group_channels(self.play_name)
        # channel_names = list(channel__.keys())
        # if len(channel_names) == 2:
        board = await get_board(self.play_hash_code, self.play_type)
        await start_turn_timer(self.play_hash_code, await get_next_player(
            self.play_hash_code, await get_user_from_play(self.play_hash_code, self.play_type)))

        await self.channel_layer.group_send(
            self.play_name, {
                "type": "INFO",
                "message": "successfully_connected_player",
                "board": board
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.play_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data__json = json.loads(text_data)
        Oy, Ox, curr_tur, goal = text_data__json["Oy"], text_data__json["Ox"], text_data__json["curr_tur"], \
            text_data__json["goal"]
        await upd_board(play_type=self.play_type, play_hash_code=self.play_hash_code, Oy=Oy, Ox=Ox, curr_tur=curr_tur, )
        if await check_board(play_type=self.play_type,
                          play_hash_code=self.play_hash_code,
                          Oy=Oy,
                          Ox=Ox,
                          curr_tur=curr_tur,
                          goal=goal):
            await self.channel_layer.group_send(
                self.play_name, {
                    "type": 'PLAY',
                    "message": 'winner',
                    "player": curr_tur
                }
            )
        else:
            await start_turn_timer(self.play_hash_code, await get_next_player(
            self.play_hash_code, await get_user_from_play(self.play_hash_code, self.play_type)).pk)

    async def INFO(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": 'INFO',
            "message": message
        }))