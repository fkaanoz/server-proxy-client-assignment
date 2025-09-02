from store.store import set_item_at, print_store

def set_handler(params, conn_to_serv=None, LOCK=None):
    inds, data = params
    

    for i in range(len(inds)):
        set_item_at(inds[i], data[i])

    req = construct_set_request(inds, data)
    
    LOCK.acquire()
    conn_to_serv.sendall(bytes(req, 'utf-8'))
    dataReceived = conn_to_serv.recv(1024)
    LOCK.release()

    dataReceived = dataReceived.decode('utf-8')

    print("\n")
    print_store()
    return dataReceived


def construct_set_request(inds, data):
    req = "SET IND="
    for i in range(len(inds)):
        req += inds[i] + ","

    # remove the last comma     
    req = req[:-1] + " DATA="

    for i in range(len(data)):
        req += data[i] + ","

    req = req[:-1] + ";"
    
    return req
