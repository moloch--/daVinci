#!/usr/bin/env python

import urllib2

class network():
    
    def __init__(self):
        self.page = []
        self.xmlItems = {}
    
    def getPage(self, url):
        ''' Get web page from url, data is stored in self.page '''
        self.page = []
        request = urllib2.Request(url)
        connection = urllib2.urlopen(request)
        while True:
            data = connection.read(1024)
            if not len(data):
                break
            print ' [<] Got %d byte(s) from %s' % (len(data), url)
            self.page.append(data)
    
    def getFile(self, url, saveTo):
        ''' Download a remote file from url and writes it to "saveTo" '''
        remoteSite = urllib2.urlopen(url)
        file = open(saveTo, 'w')
        meta = remoteSite.info()
        fileSize = int(meta.getheaders('Content-Length')[0])
        print ' [<] Downloading: %s' %saveTo.split('\\')[-1],
        fileSize_dl = 0
        block = 1024
        while True:
            buffer = remoteSite.read(block)
            if not buffer:
                break
            fileSize_dl += block
            file.write(buffer)
            status = r'[%3.0f%%] %10d bytes' % (fileSize_dl * 100. / fileSize, fileSize_dl)
            status = status + chr(8)*(len(status)+1)
            print status,
        print '\n [*] Download Completed!'
        file.close()
            
    def __getXmlItems__(self, xml):
        ''' Used to help parse the XML from twitter '''
        self.xmlItems = {}
        item = xml[xml.find('<item>')+len('<item>'):xml.find('</item>')]
        self.xmlItems['bidding'] = self.getXmlValue('<description>', '</description>', item)
        self.xmlItems['time'] = self.getXmlValue('<pubDate>', '</pubDate>', item)
        
    def getXmlValue(self, start, end, item, strip=True):
        ''' Used to retrieve a value from the XML data '''
        startIndex = item.find(start)+len(start)
        endIndex = item.find(end)
        if strip:
            return item[startIndex:endIndex]
        else:
            return item[startIndex-len(start):endIndex+len(end)]
        
    def parseXml(self, url):
        ''' Used to parse the XML from twitter '''
        self.getPage(url)
        if self.page != None:
            xml = ''.join(self.page)
            self.__getXmlItems__(xml)
            print ' [*] Got update, posted at: %s' % self.xmlItems['time']
        else:
            print ' [!] Unable to get the page through the tubes.'