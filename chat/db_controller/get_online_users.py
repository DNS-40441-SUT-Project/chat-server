from ..models import User


def get_online_users():
    return User.objects.filter(is_online=True).values()
