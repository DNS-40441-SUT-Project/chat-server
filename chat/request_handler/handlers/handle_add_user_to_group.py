from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import authenticated_user, add_member
from chat.exceptions import SecurityException
from chat.models import Group, User
from chat.utils.signature import sign_data
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_add_user_to_group(conn: ServerNormalSocketConnection, message: SocketMessage):
    user = authenticated_user(**message.headers['authentication'])
    other_username = message.body['other_username']
    sender_symmetric_key = PollConnections.get(user.username).encoded_symmetric_key
    if not (Group.objects.filter(admin_id=user.id, id=int(message.body['group_id'])).exists() and User.objects.filter(
            username=other_username).exists()):
        signature_value = '400'
        conn.send_sym_encrypted(
            path='400',
            data=dict(
                status=signature_value,
            ),
            headers=dict(
                signature_value=signature_value,
                signature=sign_data(signature_value),
                T=datetime.now().timestamp(),
            ),
            symmetric_key=PollConnections.get(user.username).encoded_symmetric_key
        )
        return
    signature_value = '200'
    conn.send_sym_encrypted(
        path='200',
        data=dict(
            status=signature_value,
        ),
        headers=dict(
            signature_value=signature_value,
            signature=sign_data(signature_value),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=sender_symmetric_key
    )
    other_user = User.objects.get(username=other_username)

    new_message = conn.recieve_sym_decrypted(symmetric_key=sender_symmetric_key)
    if user.username != authenticated_user(**new_message.headers['authentication']).username:
        raise SecurityException()
    poll_connection_context = PollConnections.get(other_username)
    poll_connection = poll_connection_context.poll_connection

    poll_connection.send_encrypted(
        path='group_secret',
        headers=dict(
            T=datetime.now().timestamp(),
        ),
        public_key=other_user.pub.rsa_public_key,
    )

    other_symmetric_key = poll_connection_context.encoded_symmetric_key
    poll_connection.recieve_sym_decrypted(symmetric_key=other_symmetric_key)
    poll_connection.send_sym_encrypted(
        path='200',
        headers=dict(
            signature_value=signature_value,
            signature=sign_data(signature_value),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=other_symmetric_key,
        data=dict(
            sender_username=user.username,
            group_secret=new_message.body['M'],
            group=message.body['group_id'],
        )
    )
    conn.send_sym_encrypted(
        path='200',
        data=dict(
            status=signature_value,
        ),
        headers=dict(
            signature_value=signature_value,
            signature=sign_data(signature_value),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=sender_symmetric_key
    )

