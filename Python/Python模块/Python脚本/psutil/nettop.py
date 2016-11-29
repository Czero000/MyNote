#!/usr/bin/env python
# encoding: UTF-8
'get system info  and network info'
import sys
import os
import atexit
import time
import psutil

time.sleep(3)

line_num = 1

# function of get cpu state


def getCPUstate(interval=1):
    return (" CPU: " + str(psutil.cpu_percent(interval)) + "%")

# function of get memory


def getMemorystate():
    phymem = psutil.virtual_memory()
    line = "Memroy: %5s%% %6s %s" % (
        phymem.percent,
        str(int(phymem.used/1024/1024))+"M",
        str(int(phymem.total/1024/1024))+"M"
    )
    return line

# bytes 2 human


def bytes2human(n):
    """
    >>> bytes2human(10000)
    9.8 k
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f %s' % (value, s)
    return '%.2fB' % (n)


def poll(interval):
    """
    Retrieve raw stats within an interval window.
    """
    total_before = psutil.net_io_counters()
    pnic_before = psutil.net_io_counters(pernic=True)
    # sleep some time
    time.sleep(interval)
    total_after = psutil.net_io_counters()
    pnic_after = psutil.net_io_counters(pernic=True)
    # get cpu state
    cpu_state = getCPUstate(interval)
    # get memory
    memory_state = getMemorystate()
    return (total_before, total_after, pnic_before, pnic_after, cpu_state, memory_state)

# refresh window


def refresh_window(total_before, total_after, pnic_before, pnic_after, cpu_state, memory_state):
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

    # print currnet time
    print  time.asctime() + " | " + cpu_state + " | " + memory_state

    # totals
    print 'NetStates:'
    print "Total Bytes: sent: %-10s received: %s" % (bytes2human(total_after.bytes_sent), bytes2human(total_after.bytes_recv))
    print "Total Packets: sent: %-10s received: %s" % (total_after.packets_sent,  total_after.packets_recv)

    # per-network interface details: let's sort network interface so that that the ones which
    # generated more traffic are shown first
    print ""
    nic_names = pnic_after.keys()
    # nic_name.sort(key=lambda x: sum(pnic_after[x], reverse=True))
    for name in nic_names:
        stats_before = pnic_before[name]
        stats_after = pnic_after[name]
        templ = "%-15s %15s %15s"
        print templ % (name, "Total", "PER_SEC")
        print templ % (
            "bytes_sent", bytes2human(stats_after.bytes_sent),
            bytes2human(
                stats_after.bytes_sent - stats_before.bytes_sent) + '/s'
        )
        print templ % (
            "bytes_recv", bytes2human(stats_after.bytes_recv),
            bytes2human(
                stats_after.bytes_recv - stats_before.bytes_recv) + '/s'
        )
        print templ % (
            "packets_sent", stats_after.packets_sent,
            stats_after.packets_sent - stats_before.packets_sent
        )
        print templ % (
            "packets_recv", stats_after.packets_recv,
            stats_after.packets_recv - stats_before.packets_recv
        )
        print " "

if __name__ == '__main__':

    try:
        interval = 0
        while True:
            args = poll(interval)
            refresh_window(*args)
            interval = 1
    except (KeyboardInterrupt, SystemExit):
        pass
