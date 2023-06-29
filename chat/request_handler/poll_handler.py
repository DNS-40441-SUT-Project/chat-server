from connection_utils.socket_message import SocketMessage
from cryptography.fernet import Fernet

from chat.data import PollConnections, LoginUserContext
from chat.db_controller import login, authenticated_user
from chat.utils.socket_connection import ServerPollConnection


def handle_poll_request(conn: ServerPollConnection, message: SocketMessage):
    if message.path == 'login':
        try:
            user = login(**message.body)
            key = Fernet.generate_key()
            PollConnections.add(user.username, LoginUserContext(conn, key.decode('utf-8')))
            conn.send('login', data={'status': '200'})
        except Exception as e:
            conn.send('login', data={'status': '400', 'msg': 'Log in Failed'})
    elif message.path == 'symmetric_key':
        try:
            user = authenticated_user(**message.body)
            symmetric_key = PollConnections.get(user.username).symmetric_key
            conn.send_encrypted(path='symmetric_key', data=dict(symmetric_key=symmetric_key),
                                public_key=user.pub.rsa_public_key)
        except Exception as e:
            conn.send('symmetric_key', data={'status': '400', 'msg': 'Not Authenticated'})

    # todo: update connections_map
    pass
