from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import authenticated_user
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_symmetric_key(conn: ServerNormalSocketConnection, message: SocketMessage):
    try:
        user = authenticated_user(**message.headers['authentication'])
        symmetric_key = PollConnections.get(user.username).symmetric_key
        conn.send_encrypted(path='symmetric_key', data=dict(symmetric_key=symmetric_key),
                            public_key=user.pub.rsa_public_key)
    except Exception:
        conn.send('symmetric_key', data={'status': '400', 'msg': 'Not Authenticated'})
