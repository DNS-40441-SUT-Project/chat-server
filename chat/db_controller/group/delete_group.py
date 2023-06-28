from django.shortcuts import get_object_or_404

from ...models import Group


def delete_group(group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    group.delete()
    return group
    # todo: send to all of clients that this group is deleted
