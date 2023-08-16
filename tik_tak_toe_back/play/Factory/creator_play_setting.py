from .absract_creator_play import Creator


async def CreatePlay(creator: Creator, type_play: str):
    return await creator.operation_create_object(type_play)
