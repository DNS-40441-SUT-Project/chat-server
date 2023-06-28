from django.db import models

from ..models.base import BaseModel


class PuPrKey(BaseModel):
    user = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='pu_pr_keys',
        unique=True,
    )

    # everyone can see this
    public_key = models.TextField()
