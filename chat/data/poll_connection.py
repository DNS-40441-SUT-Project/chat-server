import dataclasses
from typing import Dict, Tuple

from chat.utils.socket_connection import ServerPollConnection


@dataclasses.dataclass
class LoginUserContext:
    poll_connection: ServerPollConnection
    symmetric_key: str

    @property
    def encoded_symmetric_key(self):
        return self.symmetric_key.encode('utf-8')


class PollConnections:
    _all_poll_connections: Dict[str, LoginUserContext] = {}

    @classmethod
    def get(cls, username: str) -> LoginUserContext:
        return cls._all_poll_connections.get(username)

    @classmethod
    def add(cls, username: str, context: LoginUserContext):
        cls._all_poll_connections[username] = context

    @classmethod
    def remove(cls, username: str):
        cls._all_poll_connections.pop(username, None)

    @classmethod
    def clear(cls):
        cls._all_poll_connections.clear()
