import tkinter
import paramiko
import re
import time
import datetime
import subprocess
from tkinter import ttk
import sys

def status():
    my_progress["value"] = 20
    get_pcap()
    window.update_idletasks()

def get_pcap():
    global filename
    global seconds
    global eth
    global path
    today = datetime.datetime.now().strftime("%Y%m%d")
    filename = "DDNA-" + today + ".pcap"
    my_progress.start(10)
    window.update_idletasks()
    path = path_var.get()
    seconds=int(seconds_var.get())
    hostname = hostname_var.get()
    eth = find_eth(hostname,path)
    my_progress["value"] = 70
    window.update_idletasks()
    window.update()
    collect_pcap(hostname, eth, filename, seconds, path)
    cmd = f"del {path}\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return None

def find_eth(hostname,path):
    try:
        global ho
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        ftp=ssh.open_sftp()
        my_progress.step(20)
        window.update_idletasks()
        ddnalab = tkinter.Label(window,text=f"ftp connection estabilished collecting NIC card value for DDNA\n")
        ddnalab.pack()
        ftp.get("/etc/hosts",path+"\\hosts.txt")
        ftp.close()
        ssh.close() # close connection
        patt = r"DDNA-eth\d"
        fo = open(path+"\\hosts.txt", "r") # open hosts file in read mode
        files_lines = fo.readlines() # readlines create a list with each line of the file
        for each_line in files_lines:     # loop into list created
            if re.findall(patt, each_line):   # only print when you fine key word DDNA
                eth=(each_line[-6]+each_line[-5]+each_line[-4]+each_line[-3]+each_line[-2]).strip("-")
                break
        fo.close()
        ddnalab2 = tkinter.Label(window,text=f"Reading completed: NIC for DDNA is {eth}\n")
        ddnalab2.pack()
        my_progress["value"] = 30
        window.update_idletasks()
        window.update()
        time.sleep(5)
        tcpdump_installation(hostname)
        return str(eth)
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.pack()
        window.update()
    finally:
        my_progress.stop()
        

def tcpdump_installation(hostname):
   try:
       ssh = paramiko.SSHClient()  # create ssh client
       ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
       ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
       tcpdumpLab = tkinter.Label(window, text=f"Checking tcpdump version installed on remote server\n")
       tcpdumpLab.pack()
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
           tcpdumpLab = tkinter.Label(window, text=f"The version installed is: {line}\n")
           tcpdumpLab.pack()
       else:
         tcpdumpLab2 = tkinter.Label(window, text=f"tcpdump not installed on your machine installing now\n")
         tcpdumpLab2.pack()
         window.update()
         stdin, stdout, stderr = ssh.exec_command("yum -y install tcpdump")
         time.sleep(20)
         window.update()
         tcpdumpLab3 = tkinter.Label(window, text=f"Installation completed\n")
         tcpdumpLab3.pack()
         window.update()
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
            tcpdumpLab = tkinter.Label(window, text=f"The version installed is: {line}\n")
            tcpdumpLab.pack()
            ssh.close()
         my_progress["value"] = 40
         window.update_idletasks()
         window.update()
         return None
   except Exception as e:
       err = tkinter.Label(window, text=f"{e}\n")
       err.pack()
       window.update()
   finally:
       my_progress.stop()

def collect_pcap(hostname,eth,filename,seconds,path):
   try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        stdin, stdout, stderr = ssh.exec_command(f"tcpdump -i  {eth}  port  7777 -w {filename}")
    #    pcapLab = tkinter.Label(window, text=f"Capturing {filename}\n")
    #    pcapLab.pack()
        pcapLab = tkinter.Label(window, text=f"Please wait whilst capturing pcap file on DDNA\n")
        pcapLab.pack()
        window.update_idletasks()
        window.update()
        time.sleep(seconds)
        stdin, stdout, stderr = ssh.exec_command("pkill -f tcpdump")
        pcapLab2 = tkinter.Label(window, text=f"{filename} capture completed\n")
        pcapLab2.pack()
        my_progress["value"] = 60
        window.update_idletasks()
        window.update()
        ftp = ssh.open_sftp()
        pcapLab3 = tkinter.Label(window, text=f"ftp connection established downloading {filename}\n")
        pcapLab3.pack()
        my_progress["value"] = 80
        window.update_idletasks()
        window.update()
        ftp.get(filename,path+"\\"+filename)
        ftp.close()
        ssh.close()  # close connection
        pcapLab5 = tkinter.Label(window, text=f"Download completed, you can find your {filename} at {path}\n \n\n CLOSE THE WINDOW TO END THE SCRIPT")
        pcapLab5.pack()
        cmd = f"del {path}+\\hosts.txt"
        sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        my_progress["value"] = 100
        window.update_idletasks()
        time.sleep(5)
        my_progress.stop()
        return None
   except Exception as e:
       err = tkinter.Label(window, text=f"{e}\n")
       err.pack()
       window.update()
   finally:
       my_progress.stop()


window=tkinter.Tk()
window.geometry("900x800")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
seconds_var=tkinter.StringVar()
window.title("DDNA PCAP CAPTURE")
label=tkinter.Label(window,text="DDNA Pcap Capture")
label.pack()

getPathLable=tkinter.Label(window,text="enter your path: ",font=('calibre', 10, 'normal'))
getPathLable.pack()
getPathEntry=tkinter.Entry(window, textvariable=path_var,width=50,font=('calibre', 10, 'normal'))
getPathEntry.pack()
getHostLabel=tkinter.Label(window,text="enter your host ip: ",font=('calibre', 10, 'normal'))
getHostLabel.pack()
getHostEntry=tkinter.Entry(window, textvariable=hostname_var,width=15,font=('calibre', 10, 'normal'))
getHostEntry.pack()
getTimeLabel=tkinter.Label(window,text="enter pcap duration in seconds: ",font=('calibre', 10, 'normal'))
getTimeLabel.pack()
getTimeLabel=tkinter.Entry(window, textvariable=seconds_var,width=15,font=('calibre', 10, 'normal'))
getTimeLabel.pack()

my_progress = ttk.Progressbar(window, orient="horizontal", length="300", mode="determinate")
my_progress.pack(pady=20)

executeButton=tkinter.Button(window,text="Execute",command=status)
executeButton.pack()

window.mainloop()

