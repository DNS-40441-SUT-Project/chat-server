from typing import Dict

from chat.utils.socket_connection import ServerPollConnection


class LoginUserContext:
    poll_connection: ServerPollConnection
    symmetric_key: str


class PollConnections:
    _all_poll_connections: Dict[str, ServerPollConnection] = {}

    @classmethod
    def get(cls, username: str):
        return cls._all_poll_connections.get(username)

    @classmethod
    def add(cls, username: str, conn: ServerPollConnection):
        cls._all_poll_connections[username] = conn

    @classmethod
    def remove(cls, username: str):
        cls._all_poll_connections.pop(username, None)

    @classmethod
    def clear(cls):
        cls._all_poll_connections.clear()
