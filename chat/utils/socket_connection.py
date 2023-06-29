import rsa
from connection_utils.socket_connections import ServerSocketConnection
from django.conf import settings


class ServerNormalSocketConnection(ServerSocketConnection):
    _listen_port = settings.SERVER_PORT
    _limit = 10000
    my_private_key: rsa.PrivateKey = settings.PRIVATE_KEY


class ServerPollConnection(ServerSocketConnection):
    _listen_port = settings.POLL_PORT
    _limit = 10000
    my_private_key: rsa.PrivateKey = settings.PRIVATE_KEY


def accept_connection():
    return ServerSocketConnection.accept_connection()


def accept_poll_connection():
    return ServerPollConnection.accept_connection()
