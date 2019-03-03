import paramiko
import os
import json
import time
import smtplib
from email.mime.text import MIMEText

#读取当前路径
base_dir = os.getcwd()
#读取在远程主机执行的脚本
cmd_filepath = base_dir+r"\pu.txt"
cmd_file = open(cmd_filepath,"r")
cmd = cmd_file.read()
#连接远程主机
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("192.168.2.188", 23333,'root','passwd')
#执行命令
stdin, stdout, stderr = client.exec_command(cmd)
#读取信息
for line in stdout:
    global data
    data = json.loads(line)

    global cpu_percent
    allPercent = data.get('allPercent')
    if allPercent!=None:
        cpu_percent = int(allPercent)

    global mem_percent
    memPercent = data.get('memPercent')
    if memPercent!=None:
        mem_percent = int(memPercent)

    global disk_percent
    diskPercent = data.get('diskPercent')
    if diskPercent!=None:
        disk_percent = int(diskPercent)

    print(data)

#关闭连接
client.close()

class Monitor():
    #cpu_alarm
    @classmethod
    def cpu(cls, max=80):
        if cpu_percent > max:
            cls.sendMsg('cpu使用率为{:1f}%，超过了{}%，请留意。'.format(cpu_percent, max))

    #mem alarm
    @classmethod
    def mem(cls, max=10):
        if mem_percent > max:
            cls.sendMsg('内存使用率为{:1f}%，超过了{}%，请留意。'.format(mem_percent, max))

    @classmethod
    def disk(cls, max=80):
        if disk_percent > max:
            cls.sendMsg('磁盘使用率为{:1f}%，超过了{}%，请留意。'.format(disk_percent, max))

    @classmethod
    def sendMsg(cls, content):
        cls.mail(content)

    @classmethod
    def mail(cls, content):
        nickname = 'hopeMonitorSystem'

        #sendInfo
        msg_from = "yanglt7@qq.com"
        passwd = "xxx"
        subject = 'Auto alarm'

        #receiveInfo
        msg_to = "yanglt7@163.com"
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = msg_from
        msg['Subject'] = subject
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)

        try:
            server.login(msg_from, passwd)
            server.sendmail(msg_from, msg_to, msg.as_string())
            print("发送成功！")
        except Exception as ex:
            print(ex)
        finally:
            server.quit()

while True:
    Monitor.cpu(80)
    Monitor.mem(10)
    Monitor.disk(80)

    time.sleep(10)
