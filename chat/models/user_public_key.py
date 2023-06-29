from functools import cached_property

import rsa
from django.db import models

from ..models.base import BaseModel


class UserPublicKey(BaseModel):
    user = models.OneToOneField(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='pub',
    )

    key: str = models.TextField()

    @cached_property
    def rsa_public_key(self) -> rsa.PublicKey:
        return rsa.PublicKey.load_pkcs1(self.key.encode())
