#!/usr/bin/env python

import os
import sys
import mmap
import base64
import pyexiv2
import binascii

class stegoJpeg():
    
    def __init__(self, path):
        self.imagePath = path
        self.image = pyexiv2.ImageMetadata(path)
        self.image.read() # Metadata is stored in the 'image' object
        
    def displayMetadata(self):
        print ' [*] Current image metadata:'
        for key in self.image.keys():
            print '\t[+] KEY: ', key
            
    def modifyMetaTag(self):
        self.displayMetadata()
        tag = raw_input(' [?] Tag name: ')
        try:
            print ' [*] Current value: ', self.image[tag].raw_value
            self.image[tag] = raw_input(' [?] Set new tag value: ')
        except:
            print ' [!] %s is not a valid tag, try again' % tag
            sys.exit()
        self.image.write()
        print ' [+] Wrote data to file.'
        
    def writeOffset(self, message, offset=1337):
        message = base64.encodestring(message)
        message = binascii.hexlify(message)
        print ' [*] Message is (%d bytes): %s' % (len(message), message)
        self.image['Exif.Photo.ISOSpeedRatings'] = offset
        self.image.write()
        print ' [+] Wrote new metadata to ISOSpeedRatings: %d' % offset
        file = open(self.imagePath, 'r+')
        size = os.path.getsize(self.imagePath)
        map = mmap.mmap(file.fileno(), size)
        print ' [*] File size...',
        if offset + len(message) < size:
            print 'Ok.'
            map.seek(offset)
            print ' [*] Writing byte stream, please wait...',
            for byte in message:
                map.write_byte(byte)
            map.write_byte('\x00')
        else:
            print 'too small!'
        map.close()
        print 'done!'
        
    def readOffset(self, offset=1337):
        message, byte = [], ''
        file = open(self.imagePath, 'r+')
        size = os.path.getsize(self.imagePath)
        map = mmap.mmap(file.fileno(), size)
        if offset < size:
            map.seek(offset)
            print ' [*] Reading hidden byte stream...'
            while (byte != '\x00'):
                byte = map.read_byte()
                if byte != '\x00':
                    message.append(byte)
            else:
                print ' [*] Read (%d bytes):' % len(message),
                print ''.join(message), 
                print '(%s)' % base64.decodestring(binascii.unhexlify(''.join(message)))
        else:
            print ' [!] File is too small (%d), can\'t jump to offset %s' % (size, offset)

if __name__ == '__main__':
    try:
        if not os.path.exists(sys.argv[1]):
            print ' [*] File (%s) not found.' % sys.argv[2]
            sys.exit()
        jpg = stegoJpeg(sys.argv[1])
        
        if sys.argv[2] == '--meta' or '-m' == sys.argv[2]:
            jpg.modifyMetaTag()
        elif sys.argv[2] == '--writeoff' or '-w' == sys.argv[2]:
            if len(sys.argv) == 4:
                jpg.writeOffset(sys.argv[3])
            else:
                jpg.writeOffset(raw_input(' [?] Message: '))
        elif sys.argv[2] == '--readoff' or '-r' == sys.argv[2]:
            jpg.readOffset(int(sys.argv[3]))
        elif sys.argv[2] == '--all' or '-a' == sys.argv[2]:
            jpg.displayMetadata()
    except KeyboardInterrupt:
        print '\n [*] User Exit'
        
        