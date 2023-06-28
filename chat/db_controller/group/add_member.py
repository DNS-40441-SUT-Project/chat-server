from django.shortcuts import get_object_or_404

from ...models import User, Group


def add_member(group_pk, username, admin_username):
    user = get_object_or_404(User, username=username)
    # to make sure that this group has this admin
    group = get_object_or_404(Group, pk=group_pk, admin__username=admin_username)
    group.members.add(user)
    return group
    # todo: send new member to all of the old members
