def get_input():
    print_op_table()
    operation = input("Enter the Operation type according to table above : ")
    
    while not operation.isdigit() or operation not in ["0", "1", "2", "3"]:
        print("Invalid input. Please enter a proper number. \n")
        operation = input("Enter the Operation type according to table above : ")


    match operation:
        case "0":
            inds = get_get_inds()
            return "GET IND=" + ",".join(map(str, inds)) + ";"
       
        case "1":
            inds = get_set_inds()
            data = get_set_data(len(inds))
            return "SET IND=" + ",".join(map(str, inds)) + " DATA=" + ",".join(data) + ";"
        
        case "2":
            data = get_reset_data()
            if data is None:
                return "RESET;"
            else:
                return "RESET DATA=" + data + ";"
        
        case "3":
            ind = get_evict_inds()
            if ind is None:
                return "EVICT;"
            else:
                return "EVICT IND=" + ",".join(map(str, ind)) + ";"
        
    

    return "GET "


def print_op_table():
    print("\n+-------+--------+")
    print("| Code  | Action |")
    print("+-------+--------+")
    print("|  (0)  |  GET   |")
    print("|  (1)  |  SET   |")
    print("|  (2)  | RESET  |")
    print("|  (3)  | EVICT  |")
    print("+-------+--------+")


def get_get_inds():
    inds = input("Enter the indices to get (comma separated): ")
    inds = inds.split(",")
    inds = [int(i.strip()) for i in inds]

    while not all(isinstance(i, int) for i in inds):
        print("Invalid input. Please enter a comma separated list of integers.")
        input("Enter the indices to get (comma separated): ")
        inds = inds.split(",")
        inds = [int(i.strip()) for i in inds]


    while not all(i >= 0 for i in inds):
        print("Invalid input. Please enter a comma separated list of positive integers.")
        input("Enter the indices to get (comma separated): ")
        inds = inds.split(",")
        inds = [int(i.strip()) for i in inds]


    return inds


def get_set_inds():
    inds = input("Enter the indices to set (comma separated): ")
    
    if inds.strip() == "":
        return None
    else:
        while not all(i.isdigit() for i in inds.split(",")):
            print("Invalid input. Please enter a comma separated list of integers!")
            inds = input("Enter the indices to set (comma separated): ")
        
    inds = inds.split(",")
    inds = [int(i.strip()) for i in inds]

    return inds



def get_set_data(how_many):
    data = input(f"Enter the value for {how_many} items to set (comma separated): ")
    
    while how_many != 0 and data.strip() == "":
        print("Invalid input. Please enter a comma separated list of values!")
        data = input(f"Enter the value for {how_many} items to set (comma separated): ")
    data = data.split(",")
    data = [i.strip() for i in data]

    while len(data) != how_many:
        print(f"Invalid input. Please enter exactly {how_many} values!")
        data = input(f"Enter the value for {how_many} items to set (comma separated): ")
        data = data.split(",")
        data = [i.strip() for i in data]
    
    return data
    


def get_reset_data():
    data = input("Enter the value for all table to reset or press ENTER for empty string : ")
    if data.strip() == "":
        data = None
    else:
        return data.strip()
    

def get_evict_inds():
    inds = input("Enter the indices to evict (comma separated) or press ENTER for EVICT everything : ")
    
    if inds.strip() == "":
        return None
    else:
        while not all(i.isdigit() for i in inds.split(",")):
            print("Invalid input. Please enter a comma separated list of integers!")
            inds = input("Enter the indices to evict (comma separated) or press ENTER for EVICT everything : ")
        
    inds = inds.split(",")
    inds = [int(i.strip()) for i in inds]

    return inds

    