import tkinter
import paramiko
import re
import datetime



def ErrorLogs():
    global filename
    global todaysmf
    global today
    today=datetime.datetime.now().strftime("%Y%m%d")
    filename="smf-log-files."+today+".txt"
    path=path_var.get()
    hostname=hostname_var.get()
    todaysmf=fileDownload(hostname,path,today)
    Find_Critical(todaysmf,path,today)
    Find_Warning(todaysmf,path,today)
    output = tkinter.Label(window, text=f"Completed find your files at: {path}\n \n CLOSE THE WINDOW TO END THE SCRIPT")
    output.pack()
    return None

def fileDownload(hostname,path,today):
    try:
        ssh=paramiko.SSHClient() # create ssh client
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname,username="root",password="Reuters1",port=22)
        ftp=ssh.open_sftp()
        con = tkinter.Label(window, text="ftp connection established executing")
        con.pack()
        todaysmf=ftp.get("/ThomsonReuters/smf/log/"+filename,path+"\\smf-log-files."+today+".txt")
        ftp.close()
        ssh.close() # close connection
        return todaysmf
    except Exception as e:
         err = tkinter.Label(window,text=f"{e}\n")
         err.pack()

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
         err = tkinter.Label(window,text=f"{e}\n")
         err.pack()

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
        err = tkinter.Label(window,text=f"{e}\n")
        err.pack()

window=tkinter.Tk()
window.geometry("700x500")
path_var=tkinter.StringVar()
hostname_var=tkinter.StringVar()
window.title("SMF LOGs")
label=tkinter.Label(window,text="Warning & Errors Logs")
label.pack()

getPathLable=tkinter.Label(window,text="enter your path: ",font=('calibre', 10, 'normal'))
getPathLable.pack()
getPathEntry=tkinter.Entry(window, textvariable=path_var,width=50,font=('calibre', 10, 'normal'))
getPathEntry.pack()
getHostLabel=tkinter.Label(window,text="enter your host ip: ",font=('calibre', 10, 'normal'))
getHostLabel.pack()
getHostEntry=tkinter.Entry(window, textvariable=hostname_var,width=15,font=('calibre', 10, 'normal'))
getHostEntry.pack()
executeButton=tkinter.Button(window,text="Execute",command=ErrorLogs)
executeButton.pack()



window.mainloop()


