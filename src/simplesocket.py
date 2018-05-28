#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
import time
import select

TIME_TO_WAIT = 0.1
TIMEOUT = 5
BUFFER = 1024

class simplesocket(threading.Thread):
    def __init__(self,ip,port,receive_callback,offline_callback):
        super().__init__()
        self.tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp.connect((ip,port))
        # self.tcp                    = tcp
        self.online                 = True
        self.out_queue              = []
        self.receive_callback       = receive_callback
        self.offline_callback       = offline_callback

    def sendall(self,message):
        self.tcp.sendall(message.encode())

    def notify(self,message):
        self.receive_callback(message)

    def notify_offline(self):
        self.offline_callback()

    def sendall(self,message):
        self.out_queue.append(message)

    def run(self):
        con_list = [self.tcp]
        try:
            while self.online:
                time.sleep(TIME_TO_WAIT)
                if  not self.online:
                    break
                else:
                    r,s,e = \
                        select.select(con_list,con_list,[],TIMEOUT)
                    for c in s:
                        for msg in self.out_queue:
                            c.sendall(msg.encode())
                        self.out_queue.clear()
                    for c in r:
                            msg = c.recv(BUFFER).decode('utf8')
                            if msg:
                                self.notify(msg)
                            else:
                                self.shutdown()
                                self.online = False
                                break
        except Exception as e:
            print(e)
        finally:
            if self.online:
                self.shutdown()
    
    def shutdown(self):
        self.online = False
        self.tcp.shutdown(socket.SHUT_RDWR)
        self.tcp.close()
        self.notify_offline()

    def close(self):
        if self.online:
            self.shutdown()
        self.join()
        pass




