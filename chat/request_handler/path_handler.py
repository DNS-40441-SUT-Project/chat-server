import re

import rsa
from connection_utils.socket_message import SocketMessage
from django.conf import settings

from .handlers import handle_start_session
from ..utils.socket_connection import ServerNormalSocketConnection


def handle_request(conn: ServerNormalSocketConnection, message: SocketMessage):
    if re.search('^health_check$', message.path):
        print(message.path, '\t', message.body)
        conn.send(path='health_check', data='done!')
    if re.search('^health_check_enc$', message.path):
        print(message.path, '\t', rsa.decrypt(message.body, settings.PRIVATE_KEY))
        conn.send(path='health_check', data='done!')
    if re.search('^start_session$', message.path):
        handle_start_session(message.headers, message.body)
