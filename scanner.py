import argparse
import sys
from time import perf_counter
from port_scanner_functions import make_ports_list,scan_ports,Queue
from helpers import save_result,print_ports

def cli()->None:
    """
    Command Line Interface for scanning ports aplication
    """
    parser=argparse.ArgumentParser(prog="Port Scanner",usage="python3 scanner.py target_ip " \
    "first_port_to_scan  last_port_to_scan [OPTIONS]\n" \
    "Type python3 scanner.py -h or python3 scanner.py --help for additional information",
    description="Program scans given ports of the target and returns which are open")

    #obligatory arguments
    parser.add_argument("target_ip",type=str,help="Target IP(IPv4) in dot-decimal format")
    parser.add_argument("first_port",type=int,help="Fist port to scan")
    parser.add_argument("last_port",type=int,help="Last port to scan")

    #extra arguments 
    parser.add_argument("--threads_numb","-n",type=int,
                        help="Number of threads that will be used to scan ports(default: 64)")
    parser.add_argument("--time_out","-o",type=float,
                        help="Time out for connection to a port (default: 1.0)")
    parser.add_argument("--file","-f",type=str,help="pathfile where list of " \
    "open ports will be stored (file type must be .txt)")

    parser.add_argument("--time","-t",action="store_true",
                        help="measure the execution time")
    parser.add_argument("--ratio","-r",action="store_true",
                        help="Show ratio of open ports to all scanned ports")


    arguments=parser.parse_args()
    ip:str=arguments.target_ip
    first_port:int=arguments.first_port
    last_port:int=arguments.last_port
    threads_numb:int = arguments.threads_numb if arguments.threads_numb is not None else 64
    scan_time_out:float=arguments.time_out if arguments.time_out is not None else 1.0

    try:
        ports_to_scann:Queue=make_ports_list(first_port,last_port)
    except ValueError as ex:
        print(f"Error occured:{ex}")
        sys.exit(-1)

    try:
        start:float=perf_counter()
        ports_dict:dict[int,bool]=scan_ports(ports_to_scann,ip,scan_time_out,threads_numb)
        end:float=perf_counter()

    except ValueError as ex:
        print(f"Error occured:{ex}")
        sys.exit(-1)
    open_ports:list[int]=sorted([port for port in ports_dict if ports_dict[port] is True])

    if arguments.file is not None:
        save_result(arguments.file,open_ports)

    print_ports(open_ports)

    if arguments.time:
        print(f"Execution time: {(end-start):.4f} seconds")

    if arguments.ratio:
        print(f"Ratio of open ports to all scanned ports: {(len(open_ports)/len(ports_dict))*100:.4f}%")

if __name__=="__main__":
    cli()
