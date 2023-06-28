from django.db import transaction

from ...models import User


def register(username, password):
    with transaction.atomic():
        user = User.objects.create(username=username)
        user.set_password(password)
        return user.save()
