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
    poll_connection = PollConnections.get(other_user.username).poll_connection
    # 3
    poll_connection.send_encrypted(
        path='start_session_request',
        data={'from': user.username, 'T': datetime.now().timestamp(), 'KA': data['KA']},
        public_key=other_user.pub.rsa_public_key,
    )
    # 6
    message: SocketMessage = poll_connection.recieve_sym_decrypted(
        PollConnections.get(other_user.username).encoded_symmetric_key)
    data_from_b = message.body
    if data_from_b['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    if data_from_b['to'] != user.username:
        raise SecurityException()
    if other_user.username != authenticated_user(**message.headers['authentication']).username:
        raise SecurityException()

    # 7
    conn.send_sym_encrypted(path='start_session', data={
        'from': other_username, 'T': datetime.now().timestamp(), 'KB': data_from_b['KB'],
        'M': data_from_b['M'],
    }, symmetric_key=PollConnections.get(user.username).encoded_symmetric_key)

    # 10
    message_10: SocketMessage = conn.recieve_sym_decrypted(PollConnections.get(user.username).encoded_symmetric_key)
    data_10 = message_10.body
    headers = message_10.headers
    print(headers)
    print(data_10)
    user = authenticated_user(**headers['authentication'])
    if data_10['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    if data_10['to'] != other_user.username:
        raise SecurityException()

    # 11
    poll_connection.send_sym_encrypted(
        path='resume_session',
        data={'from': user.username, 'T': datetime.now().timestamp(),
              'encrypted_hash_m': data_10['encrypted_hash_m'],
              'encrypted_m_prim': data_10['encrypted_m_prim']},
        symmetric_key=PollConnections.get(other_user.username).encoded_symmetric_key,
    )

    # 14
    message_14 = poll_connection.recieve_sym_decrypted(
        PollConnections.get(other_user.username).encoded_symmetric_key
    )  # type: SocketMessage
    data_14 = message_14.body
    if data_14['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    if data_14['to'] != user.username:
        raise SecurityException()
    if other_user.username != authenticated_user(**message_14.headers['authentication']).username:
        raise SecurityException()

    print(vars(message))

    # 15
    conn.send_sym_encrypted(
        path='resume_session',
        data={
            'from': other_username,
            'T': datetime.now().timestamp(),
            'encrypted_hash_m_prim': data_14['encrypted_hash_m_prim'],
        },
        symmetric_key=PollConnections.get(user.username).encoded_symmetric_key
    )
