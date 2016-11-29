#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"get system info"

import psutil
import os
import sys
import time
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--time", dest="time",
                    metavar="10",help="此参数可以查看当前下载占用的带宽，-t是测试时间")
parser.add_option("-d", "--deamon",
                    action="store_false",dest="deamon", default=True, help="后台运行程序")

def Sysinfo():
    Boot_Start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.BOOT_TIME))
    #time.sleep(5)
    Cpu_Usage = psutil.cpu_percent()
    RAM = int(psutil.virtual_memory().total/(1024*1024))
    RAM_Percent = psutil.virtual_memory().percent
    Swap = int(psutil.swap_memory().total/(1024*1024))
    Swap_Percent = psutil.swap_memory().percent
    Net_Sent = psutil.net_io_counters().bytes_sent
    Net_Recv = psutil.net_io_counters().bytes_recv
    Net_Spkg = psutil.net_io_counters().packets_sent
    Net_Rpkg = psutil.net_io_counters().packets_recv
    BFH = r'%g'
    print "\033[1;32m开机时间：%s\033[0m" % Boot_Start
    print "\033[1;32m当前CPU使用率：%s%s\033[0m" % (Cpu_Usage, BFH)
    print "\033[1;32m当前物理内存：%dM\t 使用率：%s%s\033[0m" % (RAM, RAM_Percent, BFH)
    print "\033[1;32mSwap内存：%sM\t 使用率： %s%s\033[0m" % (Swap, Swap_Percent, BFH)
    print "\033[1;32m：发送: %d Byte\t发送包数量%d个\033[0m" % (Net_Sent, Net_Spkg)
    print "\033[1;32m：接收: %d Byte\t接收包数量%d个\033[0m" % (Net_Sent, Net_Spkg)
    for i in psutil.disk_partitions():
        print "\033[1;32m：盘符: %s 挂载点: %s 使用率: %s%s\033[0m" % (i.device,i.mountpoint,psutil.disk_usage(i.device).percent,BFH)

def NetIO(s):
    x = 0
    sum = 0
    while True:
        if x >= s:
            break
        r1 = psutil.net_io_counters().bytes_recv
        time.sleep(1)
        r2 = psutil.net_io_counters().bytes_recv
        r = r2 - r1
        print "%.2f Kb/s " % (r/1024.0)
        sum += r
        x += 1
    result = sum / x
    print "\033[1;32m%s秒内平均速度: %.2f  kb/s \033[0m" % (x,result /1025.0)

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    if options.time:
        NetIO(int(options.time))
    else:
        Sysinfo()
