
from random import choices

def save_result(pathfile:str,data:list[int])->None:
    """
    Saving results of port scanning to a txt file
    
    :param pathfile: path to the file
    :type pathfile: str
    :param data: list of ports to write into the file
    :type data: list[int]
    """
    #Trying to open a given file
    try:
        if not isinstance(pathfile,str) or not pathfile.endswith(".txt"):
            raise ValueError
        with open(pathfile,mode="w",encoding="ascii") as file:
            for port in data:
                file.write(f"{port}\n")

    except (FileExistsError,FileNotFoundError,PermissionError,ValueError):
        #If cannot open the given file a new one with a random name is created
        print(f"ERROR Could not write data to {pathfile}")
        new_file:str="".join(choices(list("abcdefghijklmnouvprstuwxyz1234567890"),k=25))+".txt"
        with open(new_file,mode="w",encoding="ascii") as file:
            for port in data:
                file.write(f"{port}\n")
        print(f"Ports were written to {new_file}")

    return


def print_ports(open_ports:list[int])->None:
    """
    Prints ports with their type. Prints 'NO PORT IS OPEN' if list is empty
    
    :param open_ports: list of open ports
    :type open_ports: list[int]
    """
    print("-"*29)
    print("PORT NUMBER".center(14),"PORT TYPE".center(14),sep="|")
    print("-"*29)
    if not open_ports:
        print("NO PORT IS OPEN".center(29))
    port_type:str
    #Checking port type (there are three categories)
    for port in open_ports:
        if port<1024:
            port_type="Well-Known"
        elif port<49152:
            port_type="Registered"
        else:
            port_type="Dynamic/Private"
        print(f"{port}".center(14),port_type.center(14),sep="|")

if __name__=="__main__":
    print_ports([])
    print_ports([1,2,1023,1024,49151,49152,50_000,65535])
