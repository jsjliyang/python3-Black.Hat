import win32con
import win32api
import win32security

import wmi
import sys
import os

LOG_FILE = "process_monitor_log.csv"

def get_process_privileges(pid):
    try:
        # 获取目标进程的句柄
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)

        # 打开主进程的令牌
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)

        # 解析已启用权限的列表
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)

        # 迭代每个权限并输出其中以及启用的
        priv_list = []
        for priv_id, priv_flags in privs:
            # 检测权限是否已经启用
            if priv_flags == 3:
                priv_list.append(win32security.LookupPrivilegeName(None, priv_id))

    except:
        priv_list.append("N/A")

    return "|".join(priv_list)

def log_to_file(message):
    fd = open(LOG_FILE, "ab")
    message = bytes(message,encoding='utf-8')
    fd.write("%s\r\n" % message)
    fd.close()

    return

# 创建一个日志文件的头
if not os.path.isfile(LOG_FILE):
    log_to_file("Time,User,Executable,CommandLine,PID,ParentPID,Privileges")

# 初始化WMI接口
c = wmi.WMI()

# 创建进程监控器
process_watcher = c.Win32_Process.watch_for("creation")


while True:
    try:
        new_process = process_watcher()

        proc_owner  = new_process.GetOwner()
        proc_owner  = "%s\\%s" % (proc_owner[0],proc_owner[2])
        create_date = new_process.CreationDate
        executable  = new_process.ExecutablePath
        cmdline     = new_process.CommandLine
        pid         = new_process.ProcessId
        parent_pid  = new_process.ParentProcessId

        privileges  = get_process_privileges(pid)

        process_log_message = "%s,%s,%s,%s,%s,%s,%s" % (create_date, proc_owner, executable, cmdline, pid, parent_pid,privileges)

        print("%s\r\n" % process_log_message)

        log_to_file(process_log_message)

    except:
        pass
