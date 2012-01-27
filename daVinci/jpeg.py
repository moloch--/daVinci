#!/usr/bin/env python

import os
import mmap
import base64
import pyexiv2
import binascii

class stegoJpeg():
    
    def __init__(self, path):
        self.image = pyexiv2.ImageMetadata(path)
        self.image.read()
        self.imagePath = path
        
    def getMetadata(self):
        metadata = {}
        metadata['make'] = self.image['Exif.Image.Make'].raw_value
        metadata['iso'] = self.image['Exif.Photo.ISOSpeedRatings'].raw_value
        return metadata
        
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
                message = binascii.unhexlify(''.join(message)) 
                print '(%s)' % base64.decodestring(message)
        else:
            print ' [!] File is too small (%d), can\'t jump to offset' % size
        return base64.decodestring(message)
