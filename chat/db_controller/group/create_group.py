from django.shortcuts import get_object_or_404

from ...models import User, Group


def create_group(admin_username, group_name):
    user = get_object_or_404(User, username=admin_username)
    return Group.objects.create(name=group_name, admin=user)
