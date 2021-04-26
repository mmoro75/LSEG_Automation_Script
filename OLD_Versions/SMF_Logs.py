# find Critical and Warning errors on SMF file daily

import paramiko
import re
import datetime

def ErrorLogs():
    global filename
    global todaysmf
    global today
    today=datetime.datetime.now().strftime("%Y%m%d")
    filename="smf-log-files."+today+".txt"
    path=input("Please provide a path where you want your logs to be stored: ")
    hostname=input("please provide hostname-ip_address: ")
    todaysmf=fileDownload(hostname,path,today)
    Find_Critical(todaysmf,path,today)
    Find_Warning(todaysmf,path,today)
    print("Completed find your files at: ",path)
    return None

def fileDownload(hostname,path,today):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password="Reuters1",port=22)
        ftp=ssh.open_sftp()
        print("ftp connection established executing:")
        todaysmf=ftp.get("/ThomsonReuters/smf/log/"+filename,path+"\\smf-log-files."+today+".txt")
        ftp.close()
        ssh.close() # close connection
        return todaysmf
    except Exception as e:
         print(e)


def Find_Critical(todaysmf,path,today):
    try:
        patt = r"\bCritical\b"
        fo = open(path+"\\smf-log-files."+today+".txt", "r") # open host file in read mode
        fo2 = open(path+"\\Critical_log-"+today+".txt", "w") # open file in write mode
        files_lines = fo.readlines() # readlines create a list with each line of the file
        for each_line in files_lines:     # loop into list crreated
            if re.findall(patt, each_line):   # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None

    except Exception as e:
         print(e)



def Find_Warning(todaysmf,path,today):
    try:
        patt = r"\bWarning\b"
        fo = open(path+"\\smf-log-files."+today+".txt","r")  # open host file in read mode
        fo2 = open(path+"\\Warning_log-"+today+".txt","w")  # open file in write mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list crreated
            if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None

    except Exception as e:
        print(e)

ErrorLogs()

if __name__=="__ErrorLogs__":
    ErrorLogs()