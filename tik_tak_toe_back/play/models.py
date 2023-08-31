from typing import List

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.postgres.fields import ArrayField
from tik_tak_toe_back import settings

User = settings.AUTH_USER_MODEL


def default_board(board_len):
    def inner_default_board():
        return [[0 for _ in range(board_len)] for _ in range(board_len)]
    return inner_default_board


class AbstractPlay(models.Model):
    play_hash_code = models.CharField(max_length=255, blank=False)
    create_at = models.DateTimeField(auto_now=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

    class Meta:
        abstract = True

    @sync_to_async
    def check_on_end_game(self):
        return True if self.winner is not None else False

    @staticmethod
    @database_sync_to_async
    def save_play(play):
        play.save()


def default_board_3x3():
    return default_board(3)


def default_board_19x19():
    return default_board(19)


class Play3x3(AbstractPlay):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plays_as_user1_3X3')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plays_as_user2_3X3')
    board = ArrayField(ArrayField(models.IntegerField(), size=3),
                       blank=True,
                       default=default_board_3x3())

    async def get_board(self) -> List[list]:
        return self.board

    async def upd_board(self, Oy: int, Ox: int, curr_tur):
        if self.board[Oy][Ox] == 0:
            self.board[Oy][Ox] = curr_tur
            print(self.board)
            await super().save_play(self)

    async def upd_winner(self, player):
        self.winner = player
        await super().save_play(self)


class Play19x19(AbstractPlay):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plays_as_user1_19X19')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plays_as_user2_19X19')
    board = ArrayField(ArrayField(models.IntegerField(), size=19),
                       blank=True,
                       default=default_board_19x19())

    async def get_board(self) -> List[list]:
        return self.board

    async def upd_board(self, Oy: int, Ox: int, curr_tur):
        if self.board[Oy][Ox] == 0:
            self.board[Oy][Ox] = curr_tur
            await super().save_play(self)

    async def upd_winner(self, player):
        self.winner = player
        await super().save_play(self)
