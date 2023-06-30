from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.utils.signature import sign_data
from chat.utils.socket_connection import ServerNormalSocketConnection
from chat.db_controller import authenticated_user


def handle_get_online_users(conn: ServerNormalSocketConnection, message: SocketMessage):
    user = authenticated_user(**message.headers['authentication'])
    signature_value = '200'
    conn.send_sym_encrypted(
        path='result_of_online_users',
        data=dict(
            signature_value=signature_value,
            status=signature_value,
            results=[_ for _ in PollConnections.get_all_usernames() if _ != user.username]
        ),
        headers=dict(
            signature=sign_data(signature_value),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=PollConnections.get(user.username).encoded_symmetric_key
    )
