import socket
import re
import threading
import time

class EmptyRequest(Exception):
    pass

class Purple():
    def __init__(self,host, port, conn_to_serv):
        self.host = host
        self.port = port
        self.conn_to_serv = conn_to_serv
        self.handlers = {}
        self.serv_handlers = {}
        self.LOCK = threading.Lock()

    def start(self):
        print("Purple server is starting...", self.host, ":", self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print("Listening for connections...")

        # Accepting messages from server in background
        threading.Thread(target=self.recieve_from_server, args=(self.conn_to_serv, ()), daemon=True).start()
        

    def accept_connection(self):
        conn, client_address = self.socket.accept()
        print('\nConnected by', client_address)
        self.recieve(conn, client_address)
        
    
        
    def recieve(self, conn, client_address):        
        while 1:
            try:
                raw_data_recieved = conn.recv(1024)
                raw_data_recieved = raw_data_recieved.decode('utf-8')

                act, params = RequestParser(raw_data_recieved)
                resp = self.handlers[act](params, self.conn_to_serv, self.LOCK)
                
                conn.sendall(bytes(resp, 'utf-8'))

            except OSError:
                print(client_address, 'disconnected')
                break

            except EmptyRequest:
                print(client_address, 'disconnected')
                break

            except Exception:
                conn.sendall(bytes("NOT_FOUND", 'utf-8'))
                continue
            
        self.accept_connection()
    

    # ACT like a server in this case
    def recieve_from_server(self, conn, client_address):
        while 1:
            acquired = self.LOCK.acquire(blocking=False)
        
            if not acquired:
                time.sleep(0.2)  
                continue

            try:
                original_blocking_state = self.conn_to_serv.getblocking()
                self.conn_to_serv.setblocking(False)
                
                try:
                    raw_data_recieved = self.conn_to_serv.recv(1024)
                    if not raw_data_recieved:
                        continue
                    
                    raw_data_recieved = raw_data_recieved.decode('utf-8')
                    act, params = Request_Parser_for_Server(raw_data_recieved)
                

                    self.serv_handlers[act](params)

                    

                except BlockingIOError:
                    continue

                except OSError:
                    continue

                except EmptyRequest:
                    continue

                except Exception:
                    continue
            
            finally:
                self.LOCK.release()
                self.conn_to_serv.setblocking(original_blocking_state)
                time.sleep(0.4)
            
   
    # For CLIENT Handlers!
    def append_handlers(self, operation, handler):
        self.handlers[operation] = handler


    # For SERVER Handlers!
    def append_server_handler(self, operation, handler):
        self.serv_handlers[operation] = handler
    


    def close(self, conn):
        conn.close()
        self.accept_connection()


    def stop(self):
        self.socket.close()
        print("Purple server stopped...")
        


def RequestParser(raw_data):
    splitted_data = re.split(';| |=', raw_data)
    
    match splitted_data[0]:
        case "GET":
            return ("GET", re.split(',', splitted_data[2]))

        case "SET":
            return ("SET", (re.split(',', (splitted_data[2])), re.split(',', (splitted_data[4]))))

        case "RESET":
            return ("RESET", splitted_data[2] if len(splitted_data) > 2 else None)
        
        case "EVICT":
            return ("EVICT", splitted_data[2] if len(splitted_data) > 2 else None)


        case "":
            raise EmptyRequest()

        case _:
            raise Exception("Unknown action")
            


def Request_Parser_for_Server(raw_data):
    splitted_data = re.split(';| |=', raw_data)
    
    match splitted_data[0]:
        case "DIRTY":
            return ("DIRTY", re.split(',', splitted_data[2]) if len(splitted_data) > 2 else None)
        
        case "ACK":
            return ("ACK", None)
        case "NACK":
            return ("NACK", None)
        case "OK":
            return ("OK", None)
        case _:
            return (None, None)
            
