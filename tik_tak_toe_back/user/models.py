from channels.db import database_sync_to_async
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    rating = models.IntegerField(default=100)

    @staticmethod
    @database_sync_to_async
    def save_user(user):
        user.save()

    async def upd_rating(self, winner) -> None:
        self.rating += 25 if winner else (-25 if self.rating > 0 else 0)
        await self.save_user(self)
