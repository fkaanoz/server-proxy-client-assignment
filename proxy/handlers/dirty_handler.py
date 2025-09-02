from store.store import evict_all, evict_item_at, print_store


def dirty_handler(ind, LOCK=None):
    while True:
        if ind is None:
            evict_all()
        else:
            for x in ind:
                evict_item_at(x)
        break

    print_store()
    print("\n")
    return "DIRTY OK;"