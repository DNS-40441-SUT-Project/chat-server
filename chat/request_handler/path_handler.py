import re

from connection_utils.socket_message import SocketMessage

from .handlers import *
from ..utils.socket_connection import ServerNormalSocketConnection


def handle_request(conn: ServerNormalSocketConnection, message: SocketMessage):
    print(message.path, '\t', message.body)
    if re.search('^health_check$', message.path):
        conn.send(path='health_check', data='done!')
    if re.search('^get_online_users$', message.path):
        handle_get_online_users(conn, message)
    if re.search('^start_session$', message.path):
        handle_start_session(conn, message.headers, message.body)
    if re.search('^symmetric_key$', message.path):
        handle_symmetric_key(conn, message)
    if re.search('^send_message_to_user$', message.path):
        handle_message_to_user(conn, message)
    if re.search('^register$', message.path):
        handle_register(conn, message)
    if re.search('^logout$', message.path):
        handle_logout(conn, message)
    if re.search('^set_public_key$', message.path):
        handle_set_public_key(conn, message)
    if re.search('^create_group$', message.path):
        handle_create_group(conn, message)
    if re.search('^get_groups$', message.path):
        handle_get_groups(conn, message)
    if re.search('^add_user_to_group$', message.path):
        handle_add_user_to_group(conn, message)
