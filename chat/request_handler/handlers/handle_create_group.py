from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import authenticated_user, create_group
from chat.utils.signature import sign_data
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_create_group(conn: ServerNormalSocketConnection, message: SocketMessage):
    user = authenticated_user(**message.headers['authentication'])
    signature_value = '200'
    g = create_group(admin_username=user.username, group_name=message.body['group_name'])
    conn.send_sym_encrypted(
        path=str(g.id),
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
