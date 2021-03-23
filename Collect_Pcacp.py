# to collect a pcap file from desired server and dowload to your local machine

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
    filename = "DDNA_Capture-" + today + ".pcap"
    path = input("Please provide a path where you want your pcap to be stored: ")
    seconds=eval(input("how long do you want the pcap to be in seconds: "))
    hostname = input("please provide hostname-ip_address: ")
    eth = find_eth(hostname,path)
    tcpdump_installation(hostname)
    data = f"tcpdump -i  {eth}  port  7777 -w {filename}"
    collect_pcap(hostname,eth,filename,seconds,path)
    cmd=f"del {path}\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return None

def find_eth(hostname,path):
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
                eth=each_line[-5]+each_line[-4]+each_line[-3]+each_line[-2]
                break
        fo.close()
        print(f"Reading completed: NIC for DDNA is {eth}")
        return str(eth)
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
         print("installation completed")
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
   except Exception as e:
     print(e)

def collect_pcap(hostname,eth,filename,seconds,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth}  port  7777 -w {filename}")
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
    except Exception as e:
      print(e)


get_pcap()



if __name__=="__get_pcap__":
    ErrorLogs()


