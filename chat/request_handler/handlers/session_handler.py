from datetime import datetime

from chat.db_controller import authenticated_user
from chat.exceptions import SecurityException
from chat.models import User


def handle_start_session(headers, data):
    user = authenticated_user(**headers['authentication'])
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    other_user = data['to']
    User.objects.get(username=other_user)
    # TODO other user not found error
