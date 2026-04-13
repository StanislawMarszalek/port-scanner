import socket
from threading import Thread
from queue import Queue


def is_dot_decimal(ip_to_check:str)->bool:
    """
    Function to check if given string is a valid IP adress
    
    :param ip_to_check: String to check
    :type ip_to_check: str
    :return: Function returns true if the string is a valid IP adress, false otherwise
    :rtype: bool
    """

    if not isinstance(ip_to_check,str):
        raise ValueError("Input must be string")

    parts:list[str]=ip_to_check.split(".")
    if len(parts)!=4:
        return False

    for idx,numb in enumerate(parts):
        try:
            parts[idx]=int(numb)
            if parts[idx]<0 or parts[idx]>255:
                return False
        except Exception:
            return False

    return True


def make_ports_list(left_end:int,right_end:int)->Queue:

    """
    Function to make a ports list to scan
    
    :param left_end: The smallest port number
    :type left_end: int
    :param right_end: The biggest port number
    :type right_end: int
    :return: Queue that contains ports to scan from range [left_end, right_end]
    :rtype: Queue
    """

    if not isinstance(left_end,int) or left_end<0:
        raise ValueError("Left end of the range must be integer greater than -1")

    if not isinstance(right_end,int) or right_end>65535:
        raise ValueError("Right end of the range must be integer less than 65536")

    if left_end>right_end:
        raise ValueError("Right end must be greater or equal to left end of the range")

    queue_of_ports:Queue=Queue(65536)

    for port in range(left_end,right_end+1):
        queue_of_ports.put(port)

    return queue_of_ports


def scan_single_port(target_ip:str,target_port:int,time_out:float=1.0)->bool:

    """
    Function to scan a single port
    
    :param target_ip: IP of the target, must be in x.x.x.x format (Dot-decimal notation)
    :type target_ip: str
    :param target_port: Port to scan, must be number from 0 to 65535
    :type target_port: int
    :param time_out: Time out for connecting to a given port (default:one seconf)
    :type time_out: float
    :return: Return true if the port is open, false otherwise
    :rtype: bool
    """

    if not isinstance(target_port,int) or target_port<0 or target_port>65535:
        raise ValueError("Port must be integer in range [0, 65535]")

    if not isinstance(target_ip,str) or not is_dot_decimal(target_ip):
        raise ValueError("IP must be string in dot-decimal notation "
        "(x.x.x.x where x is a integer in range [0, 255])")

    with socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP) as target_sock:
        target_sock.settimeout(time_out)
        try:
            target_sock.connect((target_ip,target_port))
            return True
        except Exception:
            return False


def scan_ports(ports_list:Queue,target_ip:str,time_out:float=1.0,thread_numb:int=64)->dict[int,bool]:

    """
    Function to scan all given ports of given target
    
    :param ports_list: Queue that contains ports to scan
    :type ports_list: Queue
    :param target_ip: IP of the target, must be in x.x.x.x format (Dot-decimal notation)
    :type target_ip: str
    :param time_out: Time out for a thread to connect to a given port (default:one seconf)
    :type time_out: float
    :param thread_numb: Number of threds used to scann ports
    :type thread_numb: int
    :return: Dictionary that contains ports as keys
    :rtype: dict[int, bool]
    """

    if not isinstance(target_ip,str) or not is_dot_decimal(target_ip):
        raise ValueError("IP must be string in dot-decimal notation "
        "(x.x.x.x where x is a integer in range [0,255])")

    if not isinstance(thread_numb,int) or thread_numb<=0:
        raise ValueError("Number of threads must be integer greater than 0")

    result:dict[int,bool]={}
    def thread_scan_port()->None:
        # Funtion for threads
        nonlocal ports_list,result
        while not ports_list.empty():
            port:int=ports_list.get()
            result[port]=scan_single_port(target_ip,port,time_out=time_out)
        return

    threads:list[Thread]=[Thread(target=thread_scan_port) for _ in range(thread_numb)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return result

if __name__=="__main__":
    queue=make_ports_list(0,1023)
    scan_results=scan_ports(queue,"127.0.0.1",2.0,thread_numb=256)
    for port_numb,is_open in sorted(scan_results.items(),key=lambda x:x[0]):
        if is_open is True:
            print(f"Port number {port_numb} is open")
