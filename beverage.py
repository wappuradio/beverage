#!/usr/bin/env python

from bottle import route, template, run
import os
import time
import socket

graphite = ('127.0.0.1', 2003) 

def send_beverage(beverage, num):
    ts = int(time.time())
    ds = 'meta.%s' % beverage
    line = '%s %i %i' % (ds, num, ts)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(line, graphite)
    sock.close()

def read_beverage(beverage):
    fname = 'cur.' + beverage
    
    if not os.path.isfile(fname):
        return 0

    else:
        with open(fname, 'r') as f:
            num = f.read()
            return int(num)

def write_beverage(beverage, num):
    fname = 'cur.' + beverage
    with open(fname, 'w') as f:
        f.write(str(num))

def add_beverage(beverage):
    num = read_beverage(beverage)
    num += 1
    write_beverage(beverage, num)
    send_beverage(beverage, num)

@route('/kalja')
def kalja():
    add_beverage('beer')
    return 'OK'

@route('/limu')
def kalja():
    add_beverage('soda')
    return 'OK'

run(host='0.0.0.0', port=47666)
