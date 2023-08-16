from play.Factory.absract_creator_play import Creator
from django.apps import apps


class PlayCreator(Creator):
    async def factory_method(self, type_play: str):
        if type_play == "3x3":
            return apps.get_model("play", "Play3x3")
        elif type_play == "19x19":
            return apps.get_model("play", "Play19x19")
