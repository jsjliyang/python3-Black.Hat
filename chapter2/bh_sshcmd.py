#coding=utf-8
import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramike.SSHClient()
    # 客户端也可以使用key files
    #client.load_host_keys('/home/user/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return

ssh_command('127.0.0.1', 'username', 'password', 'id')
