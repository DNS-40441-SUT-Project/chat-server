import secrets
from datetime import datetime

from connection_utils.socket_message import SocketMessage
import rsa
from django.conf import settings

from chat.exceptions import SecurityException
from chat.models import User, UserPublicKey
from chat.utils.hash import sha1
from chat.utils.socket_connection import ServerNormalSocketConnection


def handle_set_public_key(conn: ServerNormalSocketConnection, message: SocketMessage):
    data = message.body
    username = data['username']
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()
    try:
        user = User.objects.get(username=username)
    except:
        raise SecurityException()
    conn.send(path='set_public_key')
    message: SocketMessage = conn.receive()
    public_key = message.body['public_key']
    M = secrets.token_urlsafe(16)
    conn.send_encrypted(path='set_public_key', data=dict(M=M, T=datetime.now().timestamp()), public_key=public_key)
    message: SocketMessage = conn.recieve_decrypted(settings.PRIVATE_KEY)
    data = message.body
    hash_M = data['hash_M']
    if data['T'] - datetime.now().timestamp() > 10:
        raise SecurityException()

    if hash_M != sha1(M):
        raise SecurityException()

    UserPublicKey.create_or_update_key(user=user, key=rsa.PublicKey.save_pkcs1(public_key, format='PEM').decode())
    conn.send_encrypted(path='set_public_key', data=dict(status='200', T=datetime.now().timestamp()),
                        public_key=public_key)
