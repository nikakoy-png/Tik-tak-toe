from typing import List
from play.Factory.creator_play_setting import CreatePlay
from play.Factory.play_creator import PlayCreator


async def is_player_in_game(user, play_hash_code: str, type_play: str) -> bool:
    model = await CreatePlay(PlayCreator(), type_play)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    return True if (play.user1 == user or play.user2 == user) else False


async def get_user_from_play(play_hash_code: str, type_play: str) -> list:
    model = await CreatePlay(PlayCreator(), type_play)
    play = await model.objects.select_related('user1', 'user2').aget(play_hash_code=play_hash_code)
    return [play.user1, play.user2]


async def upd_board(play_type: str, play_hash_code: str, Oy: int, Ox: int, curr_tur: int) -> None:
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    await play.upd_board(Oy, Ox, curr_tur)


async def check_status_game(play_hash_code: str, play_type: str) -> bool:
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    return await play.check_on_end_game()


async def get_board(play_hash_code: str, play_type: str) -> List[list]:
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.aget(play_hash_code=play_hash_code)
    return play.board


async def get_symbol_of_player(player, play_hash_code: str, play_type: str) -> int:
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.select_related('user1').aget(play_hash_code=play_hash_code)
    return 1 if play.user1 == player else -1


async def upd_winner(player, play_hash_code: str, play_type: str) -> None:
    model = await CreatePlay(PlayCreator(), play_type)
    play = await model.objects.select_related('user1').aget(play_hash_code=play_hash_code)

    await play.upd_winner(player)

# Object -> JSON TEXT
async def get_ser_data_user(user):
    from user.serializers import UserSerializer
    print(type(UserSerializer(user).data))
    return UserSerializer(user).data


async def get_goal_for_win_of_play(play_type: str) -> int:
    return 3 if play_type == '3x3' else 5


# of course replace it on class methods (!!!every method!!!)

async def check_board(board, Oy: int, Ox: int, goal: int) -> bool:
    curr_tur = board[Oy][Ox]

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

    if (check_line(Oy, Ox, Oy + 1, Ox - 1, goal, 1) or
            check_line(Oy, Ox, Oy + 1, Ox + 1, goal, 1) or
            check_line(Oy, Ox, Oy + 1, Ox, goal, 1) or
            check_line(Oy, Ox, Oy, Ox + 1, goal, 1)):
        return True
