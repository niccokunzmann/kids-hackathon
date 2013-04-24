#!/usr/bin/python2
import sys
import traceback
import socket
import threading
import time

BROADCAST_PORT = 13719

def get_hostnames():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', BROADCAST_PORT))
    time.sleep(0.5)
    s.setblocking(0)
    hostnames = {}
    while 1:
        try:
            hostname_port, addr = s.recvfrom(1024)
        except socket.error as e:
            if e.args[0] not in (10035,):
                traceback.print_exc()
            break
        else:
            ip = addr[0]
            hostname_port = hostname_port.rsplit(':', 1)
            if len(hostname_port) != 2:
                print 'Komische informationen erhalten von', ip, ':', hostname_port 
            hostname, port = hostname_port
            if not port.isdigit():
                print 'Komische informationen erhalten von', ip, ':', port
                continue
            port = int(port)
            hostnames[hostname] = (ip, port)
    return hostnames

hostnames = get_hostnames()
hostname_list = list(hostnames)
hostname_list.sort()

for i, hostname in enumerate(hostname_list):
    print i + 1, '\t', hostname

# selbst verbindung aufnehmen

while 1:
    host = raw_input("Wohin soll ich mich verbinden: ")
    if host == "":
        host = '1'
    if host.isdigit():
        host_index = int(host) - 1
        if len(hostname_list) <= host_index:
            print('Die Zahl ist zu hoch!')
            continue
        if host_index < 0:
            print('Die Zahl ist zu klein!')
            continue
        host, port = hostnames[hostname_list[host_index]]
    elif ':' in host:
        host, port = host.rsplit(':')
        if not port.isdigit():
            print 'Der Port am ende sollte nur aus Zahlen bestehen'
            continue
        port = int(port)
    else:
        continue
    print 'Verbinde zu IP:', host, 'auf Port:', port
    try:
        connection = socket.create_connection((host, port))
    except:
        traceback.print_exc()
        print("Ich konnte mich nicht verbinden.")
    else:
        print "verbunden!"
        print '-' * 80
        break

def write_to_stdout():
    try:
        while 1:
            #print 'empfange'
            s = connection.recv(1024)
            #print 'empfangen:', repr(s)
            if not s:
                break
            try:
                s = s.decode('utf8')
            except UnicodeDecodeError:
                pass
            try:
                sys.stdout.write(s)
            except UnicodeDecodeError:
                sys.stdout.write(repr(s)[1:-1])
            sys.stdout.flush()
    except:
        traceback.print_exc()
    print('Es kann nicht mehr angezeigt werden, was passiert.')
    sys.stdin.close()
        

thread = threading.Thread(target = write_to_stdout)
thread.deamon = True
thread.start()

while 1:
    try:
        s = sys.stdin.read(1)
    except KeyboardInterrupt:
        connection.close()
    else:
        connection.sendall(s)
