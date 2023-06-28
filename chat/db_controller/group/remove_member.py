from django.shortcuts import get_object_or_404

from ...models import User, Group


def remove_member(group_pk, username, admin_username):
    user = get_object_or_404(User, username=username)
    group = get_object_or_404(Group, pk=group_pk, admin__username=admin_username)
    group.members.remove(user)
    return group
    # todo: send group state to all of the old members
