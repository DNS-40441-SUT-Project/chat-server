import pickle
from datetime import datetime

import rsa
from connection_utils.socket_message import SocketMessage
from django.conf import settings

from chat.db_controller import register
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_register(conn: ServerNormalSocketConnection, message: SocketMessage):
    data = message.body
    try:
        user = register(data['username'], data['password'])
        data = {'status': '200', 'T': datetime.now().timestamp()}
        M = rsa.sign(pickle.dumps(data), settings.PRIVATE_KEY, 'SHA-1')
        conn.send(path='register', data=data, headers=dict(sign=M))
    except Exception as e:
        data = {'status': '400', 'msg': 'Register Failed', 'T': datetime.now().timestamp()}
        M = rsa.sign(pickle.dumps(data), settings.PRIVATE_KEY, 'SHA-1')
        conn.send(path='register', data=data, headers=dict(sign=M))
