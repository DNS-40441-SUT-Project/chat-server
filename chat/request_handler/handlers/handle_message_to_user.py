from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import authenticated_user
from chat.exceptions import SecurityException
from chat.models import User
from chat.utils.socket_connection import ServerNormalSocketConnection, ServerPollConnection


def handle_message_to_user(conn: ServerNormalSocketConnection, message: SocketMessage):
    user = authenticated_user(**message.headers['authentication'])
    sender_symmetric_key = PollConnections.get(user.username).encoded_symmetric_key
    other_username = message.body['to']
    poll_connection_context = PollConnections.get(other_username)

    if message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    if poll_connection_context is None:
        conn.send_encrypted(
            path='first_response_for_message',
            data=dict(status='400'),
            public_key=user.pub.rsa_public_key,
        )
        return
    else:
        conn.send_encrypted(
            path='first_response_for_message',
            data=dict(status='200'),
            public_key=user.pub.rsa_public_key,
        )

    other_user = User.objects.get(username=other_username)

    new_message = conn.recieve_sym_decrypted(symmetric_key=sender_symmetric_key)
    if user.username != authenticated_user(**new_message.headers['authentication']).username:
        raise SecurityException()

    poll_connection = poll_connection_context.poll_connection
    other_symmetric_key = poll_connection_context.encoded_symmetric_key

    poll_connection.send_encrypted(
        path='message_from_user',
        data={
            'T': datetime.now().timestamp(),
        },
        public_key=other_user.pub.rsa_public_key,
    )

    other_user_message = poll_connection.recieve_sym_decrypted(symmetric_key=other_symmetric_key)

    if other_username != authenticated_user(**other_user_message.headers['authentication']).username:
        raise SecurityException()
    if other_user_message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    poll_connection.send_sym_encrypted(
        path='message_from_user',
        data={
            'from': user.username,
            'encrypted_M': new_message.body['encrypted_M'],
            'T': datetime.now().timestamp(),
        },
        symmetric_key=other_symmetric_key,
    )

    other_user_received_successfully_message = poll_connection.recieve_sym_decrypted(symmetric_key=other_symmetric_key)
    if other_username != authenticated_user(
            **other_user_received_successfully_message.headers['authentication']
    ).username:
        raise SecurityException()
    if other_user_received_successfully_message.body['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    conn.send_sym_encrypted(
        path='message has been sent successfully!',
        data=dict(status='200'),
        symmetric_key=sender_symmetric_key,
    )
