import paramiko
import re
import time
import datetime
import subprocess


def get_pcap():
    global filename
    global seconds
    global eth
    global path
    today = datetime.datetime.now().strftime("%Y%m%d")
    path = input("Please provide a path where you want your pcap to be stored: ")
    seconds=eval(input("how long do you want the pcap to be in seconds: "))
    hostname = input("please provide hostname-ip_address: ")
    eth = input("please specify where do you want to collect Pcap from: DDNA or EXCHA:")
    if eth.upper() == "DDNA":
       eth_ddn = find_eth_ddna(hostname,path)
       tcpdump_installation(hostname)
       filename = "DDNA_Capture-" + today + ".pcap"
       collect_pcap_ddna(hostname, eth_ddn, filename, seconds, path)

    elif eth.upper() == "EXCHA":
        eth_exch = find_eth_exch(hostname, path)
        tcpdump_installation(hostname)
        filename = "EXCHA_Capture-" + today + ".pcap"
        collect_pcap_exch(hostname,eth_exch,filename,seconds,path)
    else:
        print("please provide correct NIC card where you want Pcap from: DDNA or EXCHA")
        get_pcap()

    cmd=f"del {path}\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return None

def find_eth_ddna(hostname,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        ftp=ssh.open_sftp()
        print("ftp connection estabilished collecting NIC card value for DDNA")
        ftp.get("/etc/hosts",path+"\\hosts.txt")
        ftp.close()
        ssh.close() # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt = r"DDNA-eth\d"
        fo = open(path+"\\hosts.txt", "r") # open hosts file in read mode
        files_lines = fo.readlines() # readlines create a list with each line of the file
       # print(files_lines)
        for each_line in files_lines:     # loop into list created
            if re.findall(patt, each_line):   # only print when you fine key word DDNA
                eth_ddn=(each_line[-6]+each_line[-5]+each_line[-4]+each_line[-3]+each_line[-2]).strip("-")
                break
        fo.close()
        print(f"Reading completed: NIC for DDNA is {eth_ddn}")
        return str(eth_ddn)
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except Exception as e:
        print(e)


def find_eth_exch(hostname,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        ftp=ssh.open_sftp()
        print("ftp connection estabilished collecting NIC card value for EXCHA")
        ftp.get("/etc/hosts",path+"\\hosts.txt")
        ftp.close()
        ssh.close() # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt = r"EXCHIPA-eth\d"
        fo = open(path+"\\hosts.txt", "r") # open hosts file in read mode
        files_lines = fo.readlines() # readlines create a list with each line of the file
       # print(files_lines)
        for each_line in files_lines:     # loop into list created
            if re.findall(patt, each_line):   # only print when you fine key word DDNA
                eth_exch=(each_line[-6]+each_line[-5]+each_line[-4]+each_line[-3]+each_line[-2]).strip("-")
                break
        fo.close()
        print(f"Reading completed: NIC for DDNA is {eth_exch}")
        return str(eth_exch)
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except Exception as e:
        print(e)

def tcpdump_installation(hostname):
   try:
       ssh = paramiko.SSHClient()  # create ssh client
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
       print("Checking tcpdump version installed on remote server")
       stdin, stdout, stderr = ssh.exec_command("tcpdump --help")
       file_lines = stderr.readlines()
       patt = r"\btcpdump version\b"
       for line in file_lines:
         if re.findall(patt, line):
            line
            break
         else:
            line = ""

       if bool(line) == True:
         print("The version installed is:", line)
       else:
         print("tcpdum not installed on your machine installing now")
         stdin, stdout, stderr = ssh.exec_command("yum -y install tcpdump")
         time.sleep(20)
         print("Installation completed")
         stdin, stdout, stderr = ssh.exec_command("tcpdump --help")
         file_lines = stderr.readlines()
         patt = r"\btcpdump version\b"
         for line in file_lines:
             if re.findall(patt, line):
                 line
                 break
             else:
                 line = ""
         if bool(line) == True:
            print("The version installed is:", line)
            ssh.close()
         return None
   except ConnectionError:
       print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
   except ConnectionRefusedError:
       print("connection is refused make sure password for the server is correct")
   except Exception as e:
       print(e)

def collect_pcap_ddna(hostname,eth_ddn,filename,seconds,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth_ddn} port 7777 -w {filename}")
        print(f"Capturing {filename}")
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        print(f"{filename} capture completed")
        ftp = ssh.open_sftp()
        print(f"ftp connection established downloading {filename}")
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        print(f"Download completed, you can find your {filename} at {path}")
        return None
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except Exception as e:
        print(e)

def collect_pcap_exch(hostname,eth_exch,filename,seconds,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth_exch} -w {filename}")
        print(f"Capturing {filename}")
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        print(f"{filename} capture completed")
        ftp = ssh.open_sftp()
        print(f"ftp connection established downloading {filename}")
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        print(f"Download completed, you can find your {filename} at {path}")
        return None
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except Exception as e:
        print(e)

get_pcap()



if __name__=="__get_pcap__":
    ErrorLogs()

