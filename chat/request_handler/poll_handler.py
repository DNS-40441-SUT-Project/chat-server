from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import login, authenticated_user
from chat.utils.socket_connection import ServerPollConnection


def handle_poll_request(conn: ServerPollConnection, message: SocketMessage):
    if message.path == 'login':
        try:
            user = login(**message.body)
            PollConnections.add(user.username, conn)
            conn.send('login', data={'status': '200'})
        except Exception as e:
            conn.send('login', data={'status': '400', 'msg': 'Log in Failed'})
    elif message.path == 'symmetric_key':
        try:
            user = authenticated_user(**message.body)
            conn.send_encrypted(path='symmetric_key', data=dict(symmetric_key=None), public_key=user.pub.rsa_public_key)
        except Exception as e:
            conn.send('symmetric_key', data={'status': '400', 'msg': 'Not Authenticated'})

    # todo: update connections_map
    pass
