#error handler dla funckji port scannera pretty prinyg file saver
from random import choices

def save_result(pathfile:str,data:list[str])->None:
    """
    Saving results of port scanning to a txt file
    
    :param pathfile: path to the file
    :type pathfile: str
    :param data: list of ports to write into the file
    :type data: list[int]
    """

    try:
        if not isinstance(pathfile,str) or not pathfile.endswith(".txt"):
            raise ValueError
        with open(pathfile,mode="w",encoding="ascii") as file:
            for port in data:
                file.write(f"{port}\n")

    except (FileExistsError,FileNotFoundError,PermissionError,ValueError):
        print(f"ERROR Could not write data to {pathfile}")
        new_file:str="".join(choices(list("abcdefghijklmnouvprstuwxyz1234567890"),k=25))+".txt"
        with open(new_file,mode="w",encoding="ascii") as file:
            for port in data:
                file.write(f"{port}\n")
        print(f"Ports were written to {new_file}")

    return

