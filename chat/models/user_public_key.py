from functools import cached_property

import rsa
from django.db import models

from ..models.base import BaseModel


class UserPublicKey(BaseModel):
    @classmethod
    def create_or_update_key(cls, user, key):
        qs = cls.objects.filter(user=user)
        if qs.exists():
            qs.update(key=key)
        else:
            cls.objects.create(user=user, key=key)

    user = models.OneToOneField(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='pub',
    )

    key: str = models.TextField()

    @cached_property
    def rsa_public_key(self) -> rsa.PublicKey:
        return rsa.PublicKey.load_pkcs1(self.key.encode())
