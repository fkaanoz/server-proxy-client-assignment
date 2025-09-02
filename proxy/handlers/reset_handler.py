from store.store import reset, print_store
import time

def reset_handler(data, conn_to_serv=None, LOCK=None):

    LOCK.acquire()
    if data is None:
        conn_to_serv.sendall(bytes("RESET;", 'utf-8'))
    else:
        conn_to_serv.sendall(bytes("RESET DATA=" + data + ";", 'utf-8'))

    dataReceived=conn_to_serv.recv(1024)
    dataReceived = dataReceived.decode('utf-8')
    LOCK.release()

    if dataReceived == "OK;":
        reset()
        
    print_store()

    return dataReceived
    