import re

from .handlers import *


def handle_request(conn, message):
    print(message)
    if re.search('^health_check$', message.path):
        conn.send(path='health_check', data='done!')
