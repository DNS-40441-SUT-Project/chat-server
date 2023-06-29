from datetime import datetime

from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.data import PollConnections
from chat.db_controller import authenticated_user
from chat.exceptions import SecurityException
from chat.models import User
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_start_session(conn: ServerNormalSocketConnection, headers, data):
    user = authenticated_user(**headers['authentication'])
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    other_username = data['to']
    # TODO: what if user not found or not online
    other_user: User = User.objects.get(username=other_username)
    poll_connection = PollConnections.get(other_user.username)
    poll_connection.send_encrypted(
        path='start_session_request',
        data={'from': user.username, 'T': datetime.now().timestamp(), 'KA': data['KA']},
        public_key=other_user.pub.rsa_public_key,
    )
    message: SocketMessage = poll_connection.recieve_decrypted(private_key=settings.PRIVATE_KEY)
    data_from_b = message.body
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    if data['to'] != user.username:
        raise SecurityException()

    conn.send_encrypted(path='start_session', data={
        'from': other_username, 'T': data['T'], 'KB': data_from_b['KB'],
        'M': data_from_b['M'],
    }, public_key=user.pub.rsa_public_key)

