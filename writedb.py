import pymysql
import time
import paramiko
import os
import json

while True:
    #读取当前路径
    base_dir = os.getcwd()
    #读取在远程主机执行的脚本
    cmd_filepath = base_dir+r"\pu.txt"
    cmd_file = open(cmd_filepath,"r")
    cmd = cmd_file.read()
    #监控主机信息列表
    host_list = ({'ip': '192.168.2.188', 'port': 23333, 'username': 'root', 'password': 'ylt661810'},)
    #连接远程主机
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in host_list:
        client.connect(host['ip'], host['port'], host['username'], host['password'])
        print(host['ip'])
        #执行命令
        stdin, stdout, stderr = client.exec_command(cmd)
        #读取信息
        assert isinstance(stdout, object)
    #执行命令
    stdin, stdout, stderr = client.exec_command(cmd)

    # 连接数据库
    conn = pymysql.connect("localhost", "monitor", "*hope8848", "monitordb")
    print("Opened database successfully")

    cur = conn.cursor()
    #读取信息
    for line in stdout:
        global data
        data = json.loads(line)
        print(data)

        # get cpuInfo
        print('====================cpuInfo====================')
        logicalCount = data.get('logicalCount')
        physicalCount = data.get('physicalCount')
        userFreetime = data.get('userFreetime')
        sysFreetime = data.get('sysFreetime')
        allPercent = data.get('allPercent')
        if logicalCount!=None:
            cur.execute("""INSERT INTO cpu (logicalCount, physicalCount, userFreetime, sysFreetime, allPercent) VALUES\
            ('%s', '%s', '%s', '%s', '%s')""" % (logicalCount, physicalCount, userFreetime, sysFreetime, allPercent))
            print("Insert cpuInfo successfully")

        # get memInfo
        print('====================memInfo====================')
        memTotal = data.get('memTotal')
        memAvailable = data.get('memAvailable')
        memPercent = data.get('memPercent')
        memUsed = data.get('memUsed')
        memFree = data.get('memFree')
        if memTotal!=None:
            cur.execute("""INSERT INTO mem (memTotal, memAvailable, memPercent, memUsed, memFree) VALUES \
            ('%s', '%s', '%s', '%s', '%s')""" % (memTotal, memAvailable, memPercent, memUsed, memFree))
            print("Insert memInfo successfully")

        # get diskInfo
        print('====================diskInfo====================')
        diskTotal = data.get('diskTotal')
        diskUsed = data.get('diskUsed')
        diskFree = data.get('diskFree')
        diskPercent = data.get('diskPercent')
        if diskTotal!=None:
            cur.execute("""INSERT INTO disk (diskTotal, diskUsed, diskFree, diskPercent) VALUES \
            ('%s', '%s', '%s', '%s')""" % (diskTotal, diskUsed, diskFree, diskPercent))
            print("Insert diskInfo successfully")

        # get netInfo
        print('====================netInfo====================')
        device = data.get('device')
        addrs = data.get('addrs')
        if device!=None:
            cur.execute("""INSERT INTO net (device, addrs) VALUES \
            ('%s', '%s')""" % (device[1], addrs))
            print("Insert netInfo successfully")

        # get boot_time
        print('====================boot_time====================')
        boot_time = data.get('boot_time')
        if boot_time!=None:
            cur.execute("""INSERT INTO boot_time (boot_time) VALUES \
            ('%s')""" % (boot_time))
            print("Insert boot_time successfully")

    conn.commit()
    conn.close()
    # 关闭连接
    client.close()
    time.sleep(10)