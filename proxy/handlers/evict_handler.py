from store.store import evict_all, evict_item_at, print_store

def evict_handler(ind, conn_to_serv=None, LOCK=None):
    if ind is None:
        evict_all()
    else:
        for x in ind:
            evict_item_at(x)

    print_store()
    print("\n")
    return "OK;"