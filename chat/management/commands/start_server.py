import signal

from django.conf import settings
from django.core.management.base import BaseCommand

import threading

from chat.request_handler import handle_poll_request, handle_request
from chat.utils.socket_connection import ServerPollConnection, ServerNormalSocketConnection

all_connections = []


def handle_signal(signum: int, *args):
    for conn in all_connections:
        conn.close()
    exit(0)


signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


class Command(BaseCommand):
    help = "start the server for chat app"

    def log(self, message):
        self.stdout.write(
            self.style.SUCCESS(
                message,
            ),
        )

    def log_error(self, message):
        self.stdout.write(
            self.style.ERROR(
                message,
            ),
        )

    def handle_connection(self, conn: ServerNormalSocketConnection, addr):
        self.log(f'new connection from {addr}')
        while True:
            message = conn.recieve_decrypted(settings.PRIVATE_KEY)
            if conn.is_closed:
                self.log_error(f'connection from {addr} has been closed!')
                break
            # 2
            handle_request(conn, message)

    def handle_poll_connection(self, conn: ServerPollConnection, addr):
        self.log(f'new poll connection from {addr}')
        message = conn.recieve_decrypted(settings.PRIVATE_KEY)
        handle_poll_request(conn, message)

    def thread_start_poll_connections(self):
        self.log('accepting poll connections!')
        while True:
            new_connection, addr = ServerPollConnection.accept_connection()
            all_connections.append(new_connection)
            thread = threading.Thread(target=self.handle_poll_connection, args=(new_connection, addr))
            thread.start()

    def thread_start_connections(self):
        self.log('accepting connections!')
        while True:
            new_connection, addr = ServerNormalSocketConnection.accept_connection()
            all_connections.append(new_connection)
            thread = threading.Thread(target=self.handle_connection, args=(new_connection, addr))
            thread.start()

    def handle(self, *args, **options):
        self.log('server started...')
        poll_thread = threading.Thread(target=self.thread_start_poll_connections)
        poll_thread.start()
        self.thread_start_connections()
