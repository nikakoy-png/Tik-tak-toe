from asgiref.sync import sync_to_async

from play.Factory.creator_play_setting import CreatePlay
from play.Factory.play_creator import PlayCreator


async def is_player_in_game(user, play_hash_code: str, type_play: str) -> bool:
    model = await CreatePlay(PlayCreator(), type_play)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    return True if (play.user1 == user or play.user2 == user) else False


async def get_user_from_play(play_hash_code: str, type_play: str) -> list:
    model = await CreatePlay(PlayCreator(), type_play)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    user1 = await play.user1
    user2 = await play.user2
    return [user1, user2]


async def upd_board(play_type: str, play_hash_code: str, Oy: int, Ox: int, curr_tur: int):
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    if play.board[Oy][Ox] == 0:
        play.board[Oy][Ox] = curr_tur
        play.save()


async def check_board(play_type: str, play_hash_code: str, Oy: int, Ox: int, curr_tur: int, goal: int):
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    board = play.board

    def check_line(past_Oy: int,
                   past_Ox: int,
                   next_Oy: int,
                   next_Ox: int,
                   goal: int,
                   count: int,
                   repeat=True) -> bool | int:
        if count >= goal:
            return True
        if board[next_Oy][next_Ox] == curr_tur:
            diff_Oy, diff_Ox = next_Oy - past_Oy, next_Ox - past_Ox
            return check_line(next_Oy, next_Ox, (next_Oy + diff_Oy), (next_Ox + diff_Ox), goal, count + 1, repeat)
        elif repeat:
            diff_Oy, diff_Ox = (next_Oy - past_Oy) * (-1), (next_Ox - past_Ox) * (-1)
            return check_line(next_Oy, next_Ox, (next_Oy + diff_Oy), (next_Ox + diff_Ox), goal, 0, False)
        return False

    if check_line(Oy, Ox, Oy + 1, Ox - 1, goal, 1) or check_line(Oy, Ox, Oy + 1, Ox + 1, goal, 1) \
            or check_line(Oy, Ox, Oy + 1, Ox, goal, 1) or check_line(Oy, Ox, Oy, Ox + 1, goal, 1):
        return curr_tur
