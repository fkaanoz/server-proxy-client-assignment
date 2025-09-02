
from purple.purple_server import Purple
from handlers.get_handler import get_handler
from handlers.set_handler import set_handler
from handlers.reset_handler import reset_handler
from handlers.evict_handler import evict_handler
from handlers.dirty_handler import dirty_handler
from helpers.connect_server import connect_server


HOST = '127.0.0.1'
PORT = 3000

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8081

# Connection to Server
CONN_TO_SERVER = connect_server(SERVER_HOST, SERVER_PORT)


# Create the Proxy server
PurpleServer = Purple(HOST, PORT, CONN_TO_SERVER)
PurpleServer.start()
PurpleServer.append_handlers("GET", get_handler)
PurpleServer.append_handlers("SET", set_handler)
PurpleServer.append_handlers("RESET", reset_handler)
PurpleServer.append_handlers("EVICT", evict_handler)

PurpleServer.append_server_handler("DIRTY", dirty_handler)

PurpleServer.accept_connection()        # infinite loop to accept connections