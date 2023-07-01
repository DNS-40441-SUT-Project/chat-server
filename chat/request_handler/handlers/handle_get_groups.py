from datetime import datetime

from connection_utils.socket_message import SocketMessage

from chat.data import PollConnections
from chat.db_controller import authenticated_user
from chat.models import Group
from chat.utils.signature import sign_data
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_get_groups(conn: ServerNormalSocketConnection, message: SocketMessage):
    user = authenticated_user(**message.headers['authentication'])
    signature_value = '200'
    conn.send_sym_encrypted(
        path='groups results',
        data=dict(
            status=signature_value,
            results=dict(
                owner_ones=list(Group.objects.filter(admin=user).values()),
                joined_ones=list(Group.objects.filter(members__in=[user]).values()),
            )
        ),
        headers=dict(
            signature_value=signature_value,
            signature=sign_data(signature_value),
            T=datetime.now().timestamp(),
        ),
        symmetric_key=PollConnections.get(user.username).encoded_symmetric_key
    )
