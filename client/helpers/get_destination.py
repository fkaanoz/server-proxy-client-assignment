def get_destination():
    print_dest_table()
    des = input("Where to connect : ")

    des = des.strip()

    while not des.isdigit() or des not in ["0", "1"]:
        print("Invalid input. Please enter a proper number. \n")
        des = input("Where to connect : ")
    
    return des
    


def print_dest_table():
    print("+-------+--------+")
    print("| Code  | Action |")
    print("+-------+--------+")
    print("|  (0)  | PROXY  |")
    print("|  (1)  | SERVER |")
    print("+-------+--------+")

