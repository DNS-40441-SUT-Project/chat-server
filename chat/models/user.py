from django.contrib.auth.models import AbstractUser
from django.db import models


# for register and login we have port with specific port number and etc.
class User(AbstractUser):
    is_online = models.BooleanField(default=False)

    # may we add port number because we need to know who is this client
    # port_number = models.PositiveSmallIntegerField(null=True)
    # we need to make sure who is current request from
