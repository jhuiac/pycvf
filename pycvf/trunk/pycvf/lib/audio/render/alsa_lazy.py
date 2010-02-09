#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
import alsaaudio
import threading
import time
import numpy

def chunked(stream,count):
    """Given a sequence, returns it in chunks of len(samples) or less"""
    offset = 0
    length = len(stream)
    while offset < length:
        yield stream[offset:offset+count] ## ce mot cle yield est absolument magique !
        offset = offset + count


def play(signal,rate=44100):
    import alsaaudio
    d = alsaaudio.PCM()
    d.setchannels(1)
    d.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    #signal = signal[:rate]
    d.setperiodsize(rate*2)
    d.setrate(rate)
    for s in chunked(signal,rate*2):
        print "writing %s"%len(s)
        d.write(s)


class LazyAudioSink:
    def __init__(self,rate=44100,channels=2,fps=30):
        self._rate=rate
        self._channels=channels
        self._d = alsaaudio.PCM()
        self._d.setchannels(channels)
        self._d.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self._d.setperiodsize((rate*channels)//fps)
        self._d.setrate(rate)
    def push_nowait(self,stamped_buffer):
        ## we ignore the timestamp ""
        self._d.write(stamped_buffer[0].data)
    def push(self,stamped_buffer):
        ## we ignore the timestamp ""
        tw=len(stamped_buffer[0].data)
        off=0
        while True:
            if off:
                x=self._d.write(remainingdata)
            else:
                x=self._d.write(stamped_buffer[0].data)
            x*=(2*self._channels) # get result in bytes
            if(x>=0):
                tw-=x
                off+=x
                if tw<=0:
                    return
                remainingdata=stamped_buffer[0].data[off:] # prepare audio subpart (a csubbuffer would be better...
                time.sleep(0.0001)
            else:
                print("audio error !")
                #return
#def threadbasedsoundserver():


class AlsaSoundService(threading.Thread):
    def __init__(self,rate=44100,bufsz=1000,channels=2):
        super(AlsaSoundService,self).__init__()
        self._channels=channels
        self.d = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK,alsaaudio.PCM_NONBLOCK)
        self.d.setchannels(channels)
        self.d.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.d.setperiodsize(rate*2*channels)
        self.d.setrate(rate)
        self.players=[]
        self.readers=[]
        self.cbbufferin=numpy.zeros((bufsz,channels),dtype=numpy.int16)
        self.cbbufferout=numpy.zeros((bufsz,channels),dtype=numpy.int16)
    def register_callback_player(self,cb):
        self.players.append(cb)
    def register_callback_reader(self,cb):
        self.readers.append(cb)
    def run(self):
        while True:
            if (self.readers!=[]):
                while (d.read(self.cbbufferin)) :
                    for r in self.readers:
                        r(self.cbbufferin)
            if (self.players!=[]):
                ## we have to do mixing here
                for w in self.players:
                    self.cbbufferout=w(self.cbbufferout)
                self.xwrite(self.cbbufferout)
    def xwrite(self,buffer):
        ## we ignore the timestamp ""
        tw=len(buffer.data)
        off=0
        while True:
            if off:
                x=self.d.write(remainingdata)
            else:
                x=self.d.write(buffer.data)
            x*=(2*self._channels) # get result in bytes
            if(x>=0):
                tw-=x
                off+=x
                if tw<=0:
                    return
                remainingdata=buffer.data[off:] # prepare audio subpart (a csubbuffer would be better...
#                   time.sleep(0.0001)
                _pauseevent = threading.Event( )
                _pauseevent.wait(0.1)
                #yield None
            else:
                print("audio error (write)!")
                #return

#s=AlasaSoundService()
#s.start()
