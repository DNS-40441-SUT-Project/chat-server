from datetime import datetime

from connection_utils.socket_message import SocketMessage
from cryptography.fernet import Fernet
from django.conf import settings

from chat.data import PollConnections, LoginUserContext
from chat.db_controller import login, authenticated_user
from chat.utils.signature import sign_data
from chat.utils.socket_connection import ServerPollConnection


def handle_poll_request(conn: ServerPollConnection, message: SocketMessage):
    if message.path == 'login':
        now = datetime.now().timestamp()
        try:
            user = login(**message.body)
            key = Fernet.generate_key()
            signature_value = {'status': '200', 'user_id': hash(f'{user.id}-{user.username}-{now}')}
            conn.send(
                path='login',
                data={'status': '200'},
                headers=dict(
                    signature_value=signature_value,
                    signature=sign_data(signature_value),
                    T=now,
                ),
            )
            PollConnections.add(user.username, LoginUserContext(conn, key.decode('utf-8')))
        except Exception:
            signature_value = {'status': '400', 'msg': 'Log in Failed', 'T': now}

            conn.send(
                path='login',
                data={'status': '400', 'msg': 'Log in Failed'},
                headers=dict(
                    signature_value=signature_value,
                    signature=sign_data(signature_value),
                    T=now,
                ),
            )
            message = conn.recieve_decrypted(settings.PRIVATE_KEY)
            if conn.is_closed:
                return
            handle_poll_request(conn, message)

