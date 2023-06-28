from django.db import models

from .base import BaseModel


class Group(BaseModel):
    name = models.CharField(max_length=300)

    admin = models.ForeignKey(
        to='chat.User',
        on_delete=models.CASCADE,
        related_name='owned_chat_groups',
    )

    members = models.ManyToManyField(
        to='chat.User',
        blank=True,
        related_name='chat_groups',
    )
