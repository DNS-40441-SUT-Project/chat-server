from ...models import User


def login(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            user.is_online = True
            user.save()
            return user
    except User.DoesNotExist:
        pass


class WrongAuthentication(Exception):
    pass


def authenticated_user(username, password) -> User:
    user = login(username, password)
    if not user:
        raise WrongAuthentication
    return user
