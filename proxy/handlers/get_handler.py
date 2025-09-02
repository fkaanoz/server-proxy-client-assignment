from store.store import get_item_at, print_store, add_to_store
import time

def get_handler(ind, conn_to_serv=None, LOCK=None):    
    items = [get_item_at(x) for x in ind]
    
    # for missing ones ONLY we need to get from server
    missings = []
    for i in range(len(items)):
        if items[i] is None:
            missings.append({
                "req_ind": i,
                "miss_index": ind[i]
            })
        
    if len(missings) > 0:
        miss_ind = [x["miss_index"] for x in missings]
        
        LOCK.acquire()
        conn_to_serv.sendall(bytes("GET IND=" + ",".join(miss_ind) + ";", 'utf-8'))
        dataReceived = conn_to_serv.recv(1024)
        LOCK.release()

        dataReceived = dataReceived.decode('utf-8')
        miss_items = dataReceived.split("DATA=")[1].split(";")[0].split(",")

        for i in range(len(missings)):
            items[missings[i]["req_ind"]] = miss_items[i]
        
        # add to store
        for i in range(len(missings)):
            add_to_store(missings[i]["miss_index"], miss_items[i])
        
    
    print_store()
    print("\n")
    return "OK IND=" + ",".join(ind) + " DATA=" + ",".join(items) + ";"