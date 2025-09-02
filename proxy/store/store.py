import time

store  = {
    "Index0": {
        "Origin_index": "1",
        "Origin_value": "Item1",
        "Last_access" : "17000000003",
    },
    "Index1": {
        "Origin_index": "2",
        "Origin_value": "Item2",
        "Last_access" : "17000000010",
    },
    "Index2": {
        "Origin_index": "0",
        "Origin_value": "Item0",
        "Last_access" : "17000000034",
    },
    "Index3": {
        "Origin_index": "6",
        "Origin_value": "Item6",
        "Last_access" : "1700000000",
    },
}


def get_item_at(index):
    for p_i, value in store.items():
        if value["Origin_index"] == index:
            store[p_i]["Last_access"] = str(int(time.time()))
            return value["Origin_value"]

    return None
    
def add_to_store(index, data):
    if(len(store) >= 5):
        oldest_key = min(store, key=lambda k:int(store[k]["Last_access"]))

        del store[oldest_key]

        store[oldest_key] = {
            "Origin_index": index,
            "Origin_value": data,
            "Last_access" : str(int(time.time()))
        }
    else:
        store["Index" + str(len(store))] = {
            "Origin_index": index,
            "Origin_value": data,
            "Last_access" : str(int(time.time()))
        }


def get_all_items():
    all_items = []

    for p_i, value in store.items():
        store[p_i]["Last_access"] = str(int(time.time()))
        all_items.append(value["Origin_value"])
        
    return all_items


def set_item_at(index, data):
    for _, value in store.items():

        if value["Origin_index"] == index: # found
            value["Origin_value"] = data
            return True
        

    # not found => add to store
    if(len(store) >= 5):
        oldest_key = min(store, key=lambda k:int(store[k]["Last_access"]))

        del store[oldest_key]

        store[oldest_key] = {
            "Origin_index": index,
            "Origin_value": data,
            "Last_access" : str(int(time.time()))
        }
    else:
        store["Index" + str(len(store))] = {
            "Origin_index": index,
            "Origin_value": data,
            "Last_access" : str(int(time.time()))
        }


    # TODO : also send it to SERVER 


    return True


def evict_item_at(index):
    for p_i, value in store.items():
        if value["Origin_index"] == index:
            
            del store[p_i]
            return True
    return False


def evict_all():
    store.clear()
    

def reset():
    store.clear()



def print_store():
    print("+-----------------------------------------------+")
    print("|                    STORE                      |")
    print("+-----------------------------------------------+")
    print("|    Index     |     Value   |    Last_access   |")
    print("+-----------------------------------------------+")

    for _, value in store.items():
        print("|","  " ,value["Origin_index"], "  ", "|   ", value["Origin_value"], "   |", value["Last_access"], "|")
    print("+-----------------------------------------------+")


    