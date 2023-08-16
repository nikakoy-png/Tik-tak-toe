from abc import ABC, abstractmethod


class Creator(ABC):
    @abstractmethod
    async def factory_method(self, type_play: str): pass

    async def operation_create_object(self, type_play: str):
        return await self.factory_method(type_play)
