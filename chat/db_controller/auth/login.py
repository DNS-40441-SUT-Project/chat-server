from django.shortcuts import get_object_or_404

from ...models import User


def login(username, password):
    try:
        user = get_object_or_404(User, username=username)
        if user.check_password(password):
            user.is_online = True
            user.save()
            return user
    except:
        pass
    raise Exception('invalid login')
