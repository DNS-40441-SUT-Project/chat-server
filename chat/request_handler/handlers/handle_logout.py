from datetime import datetime

from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.data import PollConnections
from chat.db_controller import authenticated_user
from ..poll_handler import handle_poll_request
from chat.utils.signature import sign_data
from chat.utils.socket_connection import ServerNormalSocketConnection
from chat.db_controller import logout


def handle_logout(conn: ServerNormalSocketConnection, message: SocketMessage):
    user = authenticated_user(**message.headers['authentication'])
    logout(**message.headers['authentication'])
    context = PollConnections.get(user.username)
    encoded_symmetric_key = context.encoded_symmetric_key
    PollConnections.remove(user.username)
    signature_value = dict(status='200')
    conn.send_sym_encrypted(
        path='logout was successful',
        data=dict(
            status=signature_value,
            signature_value=signature_value
        ),
        headers=dict(
            signature=sign_data(signature_value),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=encoded_symmetric_key,
    )
    context.poll_connection.send_encrypted(
        path='logout was successful',
        public_key=user.pub.rsa_public_key,
    )

    new_message = context.poll_connection.recieve_decrypted(settings.PRIVATE_KEY)
    if context.poll_connection.is_closed:
        return
    handle_poll_request(context.poll_connection, new_message)
