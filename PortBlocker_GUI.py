# Python script to use Portblocker on a remote server #

import tkinter
import paramiko
import re
import time
import datetime
import subprocess
from tkinter import ttk


def status():
    my_progress.start()
    my_progress["value"] = 10
    window.update_idletasks()
    portbloker()


def portbloker():
    global today
    global eth1,eth2,eth3,eth4
    global path
    path = path_var.get()
    hostname = hostname_var.get()
    install_port_blocker(hostname,path)
    server_eth = collect_NICs(hostname,path)
    eth1="".join(server_eth.get('eth1'))
    eth2="".join(server_eth.get('eth2'))
    eth3="".join(server_eth.get('eth3'))
    eth4="".join(server_eth.get('eth4'))
    my_progress["value"] = 60
    window.update_idletasks()
    window.update()
    block_Ports(hostname, eth1, eth2, eth3, eth4)
    cmd = f"del {path}\\hosts.txt"
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    remove_portblocker(hostname)
    return None


def install_port_blocker(hostname,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        ftp = ssh.open_sftp()
        print("ftp connection installing portblocker")
        installLab = tkinter.Label(window,text=f"ftp connection installing portblocker \n")
        installLab.grid(row=10, column=1)
        window.update()
        print(path + "\\portblocker.tar")
        ftp.put(path+"\\portblocker.tar", "/root/portblocker.tar")
        time.sleep(15)
        ftp.close()
        print("Upload file completed ")
        stdin, stdout, stderr = ssh.exec_command("tar -vxf portblocker.tar")
        print("portblocker.tar unzipped checking version:")
        stdin, stdout, stderr = ssh.exec_command("chmod a+x portblocker")
        stdin, stdout, stderr = ssh.exec_command("chmod a+x PortBlocker_Eng.ko")
        stdin, stdout, stderr = ssh.exec_command("./portblocker -version")

        file_out = stdout.readlines()
        for line in file_out:
            if line in file_out:
                installLab1 = tkinter.Label(window, text=f"{line} \n")
                installLab1.grid(row=11, column=1)
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                installLab2 = tkinter.Label(window, text=f"{err}\n Portblocker in not installed on your machine\n make sure 'portblocker.tar' file is in your working path")
                installLab2.grid(row=12, column=1)
                print(
                    f"{err}\n Portblocker in not installed on your machine\n make sure 'portblocker.tar' file is in your working path")
                ssh.close()
        my_progress["value"] = 30
        window.update_idletasks()
        window.update()
        return None
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=22,column=1)
        window.update()
    finally:
        my_progress.stop()


def collect_NICs(hostname,path):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        ftp = ssh.open_sftp()
        NICLab = tkinter.Label(window, text=f"ftp colletting server NICs information \n")
        NICLab.grid(row=13, column=1)
        print("ftp colletting server NICs information")
        ftp.get("/etc/hosts", path+"\\hosts.txt")
        ftp.close()
        ssh.close()  # close connection
        # patt=r"\d{1-3}.\d{1-3}.\d{1-3}.\d{1-3}" # patt tofind ip addresses
        patt1 = r"\bDDNA-eth\d"
        patt2 = r"\bDDNB-eth\d"
        patt3 = r"\bEXCHIPA-eth\d"
        patt4 = r"\bEXCHIPB-eth\d"
        fo = open(path+"\\hosts.txt", "r")  # open hosts file in read mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        server_eth = {"eth1": [], "eth2": [], "eth3": [], "eth4": []}
        for each_line in files_lines:  # loop into list created
            if re.findall(patt1, each_line):  # only print when you fine key word DDNA
                server_eth["eth1"].append(each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt2, each_line):
                server_eth["eth2"].append(each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt3, each_line):
                server_eth["eth3"].append(each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
            elif re.findall(patt4, each_line):
                server_eth["eth4"].append(each_line[-5] + each_line[-4] + each_line[-3] + each_line[-2])
        fo.close()
        print(f"NIC Card for DDNA is {server_eth.get('eth1')}")
        print(f"NIC Card for DDNB is {server_eth.get('eth2')}")
        print(f"NIC Card for EXCHA is {server_eth.get('eth3')}")
        print(f"NIC Card for EXCHB is {server_eth.get('eth4')}")
        NICLab1 = tkinter.Label(window, text=f"NIC Card for DDNA is {server_eth.get('eth1')}\n" 
                f"NIC Card for DDNB is {server_eth.get('eth2')}\n" f"NIC Card for EXCHA is {server_eth.get('eth3')}\n" f"NIC Card for EXCHB is {server_eth.get('eth4')}")
        NICLab1.grid(row=14, column=1)
        ssh.close()
        my_progress["value"] = 50
        window.update_idletasks()
        window.update()
        return server_eth
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=23,column=1)
        window.update()
    finally:
        my_progress.stop()

def block_Ports(hostname,eth,eth2,eth3,eth4):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        print("Connected to remote host")
        a = a_var.get()
        b = b_var.get()
        wait= int(seconds_var.get())
        seconds = str(wait)
        if a == "DDN" and b=="B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All DDN NIC cards traffic is blocked for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All DDN NIC cards traffic is blocked for {wait} seconds\n")
            PortLab.grid(row=18, column=1)
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "DDN" and b== "U":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on DDN NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on DDN NIC for {wait} seconds\n")
            PortLab.grid(row=18, column=1)
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "DDN" and b == "T":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth1 + " -j " + eth2 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on DDN NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on DDN NIC for {wait} seconds\n")
            PortLab.grid(row=18, column=1)
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "EXCH" and b == "B":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r B -s B -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All Exchange NIC cards traffic is blocked for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All Exchange NIC cards traffic is blocked for {wait} seconds\n")
            PortLab.grid(row=18, column=1)
            window.update()
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "EXCH" and b== "U":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r U -s U -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All UPD Traffic is blocked on Exchange NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All UPD Traffic is blocked on Exchange NIC for {wait} seconds\n")
            PortLab.grid(row=18, column=1)
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        elif a == "DDN" and b == "T":
            stdin, stdout, stderr = ssh.exec_command(
                "./portblocker -i " + eth3 + " -j " + eth4 + " -r T -s T -d B -e B -t " + seconds + " -f 1 -a")
            print(f"All TCP Traffic is blocked on Exchange NIC for {wait} seconds")
            PortLab = tkinter.Label(window, text=f"All TCP Traffic is blocked on Exchange NIC for {wait} seconds\n")
            PortLab.grid(row=18, column=1)
            time.sleep(wait + 10)
            print("Completed all the blocked channles are back on line ")
            PortLab1 = tkinter.Label(window, text=f"Completed all the blocked channles are back on line\n")
            PortLab1.grid(row=19, column=1)
            ssh.close()
        else:
            PortLab3 = tkinter.Label(window, text=f"WRONG SELECTIONS\n Your current selection is:\n NIC Cards to Block={a}\n Protocol:{b},please check all the inforamtion are correct \n")
            PortLab3.grid(row=18, column=1)
            print(f"WRONG SELECTIONS\n Your current selection is:\n NIC Cards to Block={a}\n Protocol:{b},please check all the inforamtion are correct")
            block_Ports(hostname,username,password,eth,eth2,eth3,eth4)
        ssh.close()
        my_progress["value"] = 70
        window.update_idletasks()
        return None
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=24,column=1)
        window.update()
    finally:
        my_progress.stop()

def remove_portblocker(hostname):
    try:
        ssh = paramiko.SSHClient()  # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username="root", password="Reuters1", port=22)
        stdin, stdout, stderr = ssh.exec_command("rm portblocker.tar")
        stdin, stdout, stderr = ssh.exec_command("rm portblocker")
        stdin, stdout, stderr = ssh.exec_command("rm PortBlocker_Eng.ko")
        stdin, stdout, stderr = ssh.exec_command("./portblocker -version")

        file_out = stdout.readlines()
        for line in file_out:
            if line in file_out:
                UninLab = tkinter.Label(window, text=f" {line}\n")
                UninLab.grid(row=20, column=1)
                print(line)
        file_err = stderr.readlines()
        for err in file_err:
            if err in file_err:
                UninLab = tkinter.Label(window, text=f"{err}\n Portblocker has been uninstalled\n \n\n CLOSE THE WINDOW TO END THE SCRIPT")
                UninLab.grid(row=20, column=1)
              #  print(f"{err}\n Portblocker has been uninstalled")
                ssh.close()
        my_progress["value"] = 80
        window.update_idletasks()
        time.sleep(5)
        my_progress.stop()
        return None
    except Exception as e:
        err = tkinter.Label(window, text=f"{e}\n")
        err.grid(row=25,column=1)
        window.update()
    finally:
        my_progress.stop()


window=tkinter.Tk()
window.geometry("1000x800")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
a_var=tkinter.StringVar()
b_var=tkinter.StringVar()
seconds_var=tkinter.StringVar()
window.title("PortBlocker")
label=tkinter.Label(window,text="Portblocker Configurations: ")
label.grid(row=0,column=1)
label1=tkinter.Label(window,text="!!!WARNING: make sure 'portblocker.tar' is available in your working path!!!")
label1.grid(row=1,column=1)

getPathLable=tkinter.Label(window,text="enter your path: ",font=('calibre', 10, 'normal'))
getPathLable.grid(row=2, column=0)
getPathEntry=tkinter.Entry(window, textvariable=path_var,width=30,font=('calibre', 10, 'normal'))
getPathEntry.grid(row=2, column=1)
getHostLabel=tkinter.Label(window,text="enter your host ip: ",font=('calibre', 10, 'normal'))
getHostLabel.grid(row=3,column=0)
getHostEntry=tkinter.Entry(window, textvariable=hostname_var,width=20,font=('calibre', 10, 'normal'))
getHostEntry.grid(row=3,column=1)
getTimeLabel=tkinter.Label(window,text="Enter port blocking time in seconds: ",font=('calibre', 10, 'normal'))
getTimeLabel.grid(row=4,column=0)
getTimeEntry=tkinter.Entry(window, textvariable=seconds_var,width=10,font=('calibre', 10, 'normal'))
getTimeEntry.grid(row=4,column=1)
c1 = tkinter.Checkbutton(window, text='Select Protocol UDP',variable=b_var, onvalue="U", offvalue="T")
c1.grid(row=6,column=1)
c1.deselect()
c2 = tkinter.Checkbutton(window, text='Select Protolcol TCP',variable=b_var, onvalue="T", offvalue="U")
c2.grid(row=6,column=2)
c2.deselect()

c3 = tkinter.Checkbutton(window, text='Both UDP and TCP',variable=b_var, onvalue="B", offvalue="U")
c3.grid(row=6,column=3)
c4 = tkinter.Checkbutton(window ,variable=b_var, onvalue="DDN", offvalue="B",text='Both NIC')
c4.grid(row=7,column=3)
c4.deselect()
c5 = tkinter.Checkbutton(window, text='Select NIC to BLock EXCH',variable=a_var, onvalue="EXCH", offvalue="DDN")
c5.grid(row=7,column=1)
c6 = tkinter.Checkbutton(window ,variable=a_var, onvalue="DDN", offvalue="EXCH",text='Select NIC to block DDN')
c6.grid(row=7,column=2)
c6.deselect()

executeButton=tkinter.Button(window,text="Execute",command=status)
executeButton.grid(row=8,column=1)
my_progress = ttk.Progressbar(window, orient="horizontal", length="300", mode="determinate")
my_progress.grid(row=9,column=1)


window.mainloop()


