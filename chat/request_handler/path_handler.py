import re

import rsa
from connection_utils.socket_message import SocketMessage
from django.conf import settings

from .handlers import handle_start_session, handle_symmetric_key, handle_message_to_user, handle_register, handle_set_public_key
from ..utils.socket_connection import ServerNormalSocketConnection


def handle_request(conn: ServerNormalSocketConnection, message: SocketMessage):
    print(message.path, '\t', message.body)
    if re.search('^health_check$', message.path):
        conn.send(path='health_check', data='done!')
    if re.search('^start_session$', message.path):
        handle_start_session(conn, message.headers, message.body)
    if re.search('^symmetric_key$', message.path):
        handle_symmetric_key(conn, message)
    if re.search('^send_message_to_user$', message.path):
        handle_message_to_user(conn, message)
    if re.search('^register$', message.path):
        handle_register(conn, message)
    if re.search('^set_public_key$', message.path):
        handle_set_public_key(conn, message)
