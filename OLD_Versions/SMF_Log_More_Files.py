
import paramiko
import re
import datetime


def ErrorLogs():
    global filename
    global today
    global oldFile
    global oldfilename
    global date
    today=datetime.datetime.now().strftime("%Y%m%d")
    path = input("Please provide a path where you want your logs to be stored: ")
    hostname = input("please provide hostname-ip_address: ")
    options=input("do you want to download today SMF log? Y or N: ").upper()
    if options == "Y":
        filename = "smf-log-files." + today + ".txt"
        todaysmf = fileDownload(hostname, path)
        Find_Critical(path,today)
        Find_Warning(path,today)
    else:
        date=input("please enter date fo SMF files you want to analyze format yyyy/mm/dd - i.e '20210412: ")
        oldfilename="smf-log-files."+date+"_235959.txt"
        oldsmf = Date_fileDownload(hostname, path)
        Find_Critical_oldFile(path,date)
        Find_Warning_oldfile(path, date)
    print("Completed find your files at: ",path)
    return None

def fileDownload(hostname,path):
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
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except Exception as e:
         print(e)


def Date_fileDownload(hostname,path):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password="Reuters1",port=22)
        ftp=ssh.open_sftp()
        print("ftp connection established executing:")
        oldsmf=ftp.get("/ThomsonReuters/smf/log/"+oldfilename,path+"\\smf-log-files."+date+".txt")
        ftp.close()
        ssh.close() # close connection
        return oldsmf
    except TimeoutError:
        print("connection timeout make sure Ip address is correct and you are connected to LSEG VPN")
    except FileNotFoundError:
        print("SMF file not found make sure the server ip and local path provided are correct")
    except ConnectionError:
        print("Connection Error make sure server ip provided is correct and you are connected to the LSEG VPN")
    except ConnectionRefusedError:
        print("connection is refused make sure password for the server is correct")
    except Exception as e:
        print(e)
    except Exception as e:
         print(e)


def Find_Critical_oldFile(path,date):
    try:
        patt = r"\bCritical\b"
        fo = open(path + "\\smf-log-files." + date + ".txt", "r")  # open host file in read mode
        fo2 = open(path + "\\Critical_log-" + date + ".txt", "w")  # open file in write mode
        files_lines = fo.readlines()  # readlines create a list with each line of the file
        for each_line in files_lines:  # loop into list crreated
            if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                fo2.write(each_line)  # write line on errorlog file
        fo.close()
        fo2.close()
        return None
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
    except Exception as e:
        print(e)

def Find_Critical(path, today):
        try:
            patt = r"\bCritical\b"
            fo = open(path + "\\smf-log-files." + today + ".txt", "r")  # open host file in read mode
            fo2 = open(path + "\\Critical_log-" + today + ".txt", "w")  # open file in write mode
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    fo2.write(each_line)  # write line on errorlog file
            fo.close()
            fo2.close()
            return None
        except FileNotFoundError:
            print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        except Exception as e:
             print(e)

def Find_Warning(path,today):
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
    except FileNotFoundError:
        print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
    except Exception as e:
        print(e)

def Find_Warning_oldfile(path, date):
        try:
            patt = r"\bWarning\b"
            fo = open(path + "\\smf-log-files." + date + ".txt", "r")  # open host file in read mode
            fo2 = open(path + "\\Warning_log-" + date + ".txt", "w")  # open file in write mode
            files_lines = fo.readlines()  # readlines create a list with each line of the file
            for each_line in files_lines:  # loop into list crreated
                if re.findall(patt, each_line):  # only print when you fine key word DDNA or DDNB
                    fo2.write(each_line)  # write line on errorlog file
            fo.close()
            fo2.close()
            return None
        except FileNotFoundError:
            print(f"SMF file not found make sure SMF file to analyze is downloaded at {path}")
        except Exception as e:
            print(e)

ErrorLogs()

if __name__=="__ErrorLogs__":
    ErrorLogs()