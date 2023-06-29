from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import login
from chat.utils.socket_connection import ServerPollConnection


def handle_poll_request(conn: ServerPollConnection, message: SocketMessage):
    if message.path == 'login':
        try:
            user = login(**message.body)
            PollConnections.add(user.username, conn)
            conn.send('login', data={'status': '200'})
        except Exception as e:
            conn.send('login', data={'status': '400', 'msg': 'Chert'})
    # todo: update connections_map
    pass
