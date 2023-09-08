import asyncio
import json
from collections import defaultdict
from channels.generic.websocket import AsyncWebsocketConsumer
from play.redis_services.redis_services import get_next_player, start_turn_timer, get_currently_tur, clear_data, \
    get_remaining_time
from play.services.play_factory import create_play
from play.services.play_services import is_player_in_game, get_user_from_play, check_board, upd_board, get_board, \
    get_symbol_of_player, get_goal_for_win_of_play, get_ser_data_user, check_status_game, upd_winner


class SearchPlay(AsyncWebsocketConsumer):
    search_users = set(tuple())

    async def connect(self):
        self.user = self.scope["user"]
        self.type_play = self.scope['url_route']['kwargs']['type_play']
        self.search_users.add((self.user, self.type_play))
        await self.channel_layer.group_add(str(self.user.username), self.channel_name)
        await self.accept()
        await self.check_searcher()

    async def disconnect(self, close_code):
        try:
            self.search_users.remove((self.user, self.type_play))
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
                    print(1)
                    await self.disconnect_connected_user(user[0])
                    break
                except TimeoutError as e:
                    await self.send_user_message(user[0].username, {'error': e.strerror})

    async def disconnect_connected_user(self, user):
        self.search_users.remove((self.user, self.type_play))
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
    __play = defaultdict(set)

    async def add_player_to_play(self, player):
        self.__play[self.play_name].add(player)

    async def get_player_in_play(self):
        return self.__play[self.play_name]

    async def connect(self):
        self.user = self.scope["user"]
        self.play_hash_code = self.scope["url_route"]["kwargs"]["play_hash_code"]
        self.play_type = self.scope["url_route"]["kwargs"]["play_type"]
        self.play_name = "play_%s" % self.play_hash_code

        if await check_status_game(self.play_hash_code, self.play_type):
            await self.send(text_data=json.dumps({
                "type": "ERROR",
                "message": "Game is over!"
            }))
            await self.close()

        # for reconnect
        if self.user in await self.get_player_in_play():
            await self.channel_layer.group_add(self.play_name, self.channel_name)
            await self.accept()
            board = await get_board(self.play_hash_code, self.play_type)
            curr_tur_player = await get_currently_tur(self.play_hash_code)
            await self.send(text_data=json.dumps({
                "type": "INFO",
                "message": "successfully_connected_player",
                "board": board,
                "curr_tur": await get_symbol_of_player(curr_tur_player, self.play_hash_code, self.play_type),
                "curr_player": await get_ser_data_user(self.user),
                "players": [await get_ser_data_user(user) for user in await self.get_player_in_play()]
            }))
        else:
            if not is_player_in_game:
                await self.close()

                await self.send(text_data=json.dumps({
                    "type": 'ERROR',
                    "message": 'unsuccessfull',
                    # will add exceptions
                }))

            await self.channel_layer.group_add(self.play_name, self.channel_name)
            await self.add_player_to_play(self.user)
            await self.accept()

            await self.send(text_data=json.dumps({
                "type": 'INFO',
                "message": 'successfully_connected_player',
            }))
            if len(await self.get_player_in_play()) == 2:
                curr_tur_player = await get_next_player(
                    self.play_hash_code, await get_user_from_play(self.play_hash_code, self.play_type))
                board = await get_board(self.play_hash_code, self.play_type)
                await start_turn_timer(self.play_hash_code, curr_tur_player)
                await self.send_info(board, curr_tur_player)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.play_name, self.channel_name)

    async def end_game(self, is_timer_equal_zero: bool):
        users = [user for user in await self.get_player_in_play()]
        users.remove(self.user)
        winner = self.user if not is_timer_equal_zero else users[0]

        await self.channel_layer.group_send(
            self.play_name, {
                "type": 'PLAY',
                "message": 'winner',
                "player": await get_ser_data_user(winner)
            }
        )
        await upd_winner(winner, self.play_hash_code, self.play_type)
        await asyncio.gather(*[user.upd_rating(winner=True if user == winner else False)
                               for user in await self.get_player_in_play()])
        await clear_data(self.play_hash_code, await self.get_player_in_play())

    async def receive(self, text_data=None, bytes_data=None):
        text_data__json = json.loads(text_data)
        if text_data__json['type'] == 'timerEqualZero':
            await self.end_game(is_timer_equal_zero=True)
        else:
            Oy, Ox, curr_tur = text_data__json["Oy"], text_data__json["Ox"], text_data__json["curr_tur"]
            __curr_tur = await get_symbol_of_player(self.user, self.play_hash_code, self.play_type)

            if __curr_tur == curr_tur:
                await upd_board(play_type=self.play_type, play_hash_code=self.play_hash_code, Oy=Oy, Ox=Ox,
                                curr_tur=curr_tur)
                board = await get_board(self.play_hash_code, self.play_type)
                curr_tur = await get_next_player(
                    self.play_hash_code, await get_user_from_play(self.play_hash_code, self.play_type))

                await start_turn_timer(self.play_hash_code, curr_tur)
                await self.channel_layer.group_send(
                    self.play_name, {
                        "type": "INFO",
                        "message": "successfully_connected_player",
                        "board": board,
                        "curr_tur": await get_symbol_of_player(curr_tur, self.play_hash_code, self.play_type),
                        "curr_player": await get_ser_data_user(await get_currently_tur(self.play_hash_code))
                    }
                )
                if await check_board(board=board,
                                     Oy=Oy,
                                     Ox=Ox,
                                     goal=await get_goal_for_win_of_play(self.play_type)):
                    await self.end_game(is_timer_equal_zero=False)

    async def INFO(self, event):
        message = event['message']
        board = event['board']
        curr_tur = event['curr_tur']
        curr_player = event['curr_player']
        await self.send(text_data=json.dumps({
            "type": 'INFO',
            "message": message,
            "board": board,
            "curr_tur": curr_tur,
            "curr_player": curr_player,
            "players": event['players'] if 'players' in event else None
        }))

    async def send_info(self, board, curr_tur_player):
        await self.channel_layer.group_send(
            self.play_name, {
                "type": "INFO",
                "message": "successfully_connected_player",
                "board": board,
                "curr_tur": await get_symbol_of_player(curr_tur_player, self.play_hash_code, self.play_type),
                "curr_player": await get_ser_data_user(self.user),
                "players": [await get_ser_data_user(user) for user in await self.get_player_in_play()]
            }
        )

    async def PLAY(self, event):
        message = event['message']
        player = event['player']
        await self.send(text_data=json.dumps({
            "type": 'PLAY',
            "message": message,
            "player": player
        }))

    async def ERROR(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            "type": 'ERROR',
            "message": message,
        }))


class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.play_hash_code = self.scope["url_route"]["kwargs"]["play_hash_code"]
        self.channel_name = f"timer_{self.play_hash_code}"
        await self.channel_layer.group_add(self.channel_name, self.channel_name)
        await self.accept()
        self.timer_task = asyncio.create_task(self.send_timer_update())

    async def disconnect(self, close_code):
        self.timer_task.cancel()
        await self.channel_layer.group_discard(self.channel_name, self.channel_name)

    async def send_timer_remaining(self, remaining_time):
        await self.send(text_data=json.dumps({
            "remaining_time": remaining_time
        }))

    async def send_timer_update(self):
        while True:
            remaining_time = await get_remaining_time(self.play_hash_code, await get_currently_tur(self.play_hash_code))
            await self.send_timer_remaining(remaining_time)
            await asyncio.sleep(1)
