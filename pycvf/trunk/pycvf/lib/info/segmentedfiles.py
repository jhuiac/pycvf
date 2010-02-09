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


import os
import re
import ctypes

class LargeSegmentedFile:
    """ allow 64bits access on 32bits filesystems"""
    def get_fileoffsets(self,dirname):
#        rex=re.compile(r"segment(\d+).dat")
        r=[0]
        try:
            for segment in range(0x10000):
                for subsegment in range(0x10000):
                    r.append=(os.stat(("%s/segment-%04x/%04x.dat")%(dirname,segment,subsegment))[6])
        except:
            pass
        r=numpy.ndarray(r,dtype=numpy.uint64)
        self.fileoffsets=r.cumsum()
    def lastfileid(self):
        try:
            for segment in range(0x10000):
                os.stat(("%s/segment-%04x/0000.dat")%(self.filename,segment))
        except:
            pass
        segment=segment-1
        assert(segment>=0)
        try:
            for subsegment in range(0x10000):
                os.stat(("%s/segment-%04x/%04x.dat")%(self.filename,segment,subsegment))
        except:
            pass
        subsegment=subsegment-1
        assert(subsegment>=0)
        return (segment,subsegment)
    def __init__(self,filename,mode,segmentsize=0x70000000):
        self.segmentsize=segmentsize
        self.mode=mode
        self.filename=filename
        #self.fileoffsets=[]
        if (mode[0]=='r'):
            try:
                os.stat(filename)
                self.segment=0
                self.subsegment=0
                self.fp=open("%s/segment-%04x/%04x.dat"%(self.filename,self.segment,self.subsegment),self.mode)
                self.lp=self.lastfileid()
            except:
                if (mode=="r+"):
                    mode="w+"
                else:
                    raise Exception, "unable to open file"
            #self.get_fileoffsets()
        if (mode[0]=='w'):
            try:
                os.stat(filename)
                try :
                    maxsegment,maxsubsegment=self.lastfileid()
                    print maxsegment
                    for s in range(maxsegment+1):
                        dir=(filename+"/segment-%04x"%s)
                        try:
                            for ss in range (0x10000):
                                print "removing "+("%s/%04x.dat"%(dir,ss))
                                os.remove("%s/%04x.dat"%(dir,ss))
                        except OSError:
                            pass
                        try:
                            os.rmdir(dir)
                        except OSError:
                            pass
                    os.rmdir(filename)
                except OSError:
                    os.rmdir(filename)
                    pass
            except OSError:
                pass
            os.mkdir(filename)
            os.mkdir(filename+"/segment-0000")
            self.segment=0
            self.subsegment=0
            self.fp=open("%s/segment-%04x/%04x.dat"%(self.filename,self.segment,self.subsegment),self.mode)
            self.fp.flush()
            self.lp=self.lastfileid()
        if (mode[0]=='a'):
            try:
                os.stat(filename)
            except OSError:
                os.mkdir(filename)
            try:
                os.stat(filename+"/segment-0000")
            except OSError:
                os.mkdir(filename+"/segment-0000")
            self.lp=(self.segment,self.subsegment)=self.lastfileid()
            self.fp=open("%s/segment-%04x/%04x.dat"%(self.filename,self.segment,self.subsegment),self.mode)
        if (mode[0]!='a') and (mode[0]!='r') and (mode[0]!='w'):
            raise Exception, "unknown open mode"
        self.start=[]
    def seek(self,position,whence=0):
        xwhence=whence
        if (xwhence==2):
            position=self.filesize()+position
            xwhence=0
        if (xwhence==1):
            position=self.tell()+position
            xwhence=0
        if (xwhence==0):
            csegment=position//self.segmentsize
            cseek=position%self.segmentsize
            segment=csegment//0x10000
            subsegment=csegment%0x10000
            if ((self.segment!=segment) or (self.subsegment!=subsegment)):
                self.fp.close()
                self.segment=segment
                self.subsegment=subsegment
                self.fp=open("%s/segment-%04x/%04x.dat"%(self.filename,self.segment,self.subsegment),self.mode)
            self.fp.seek(position%self.segmentsize,0)
    def filesize(self):
        if (self.lp==(self.segment,self.subsegment)):
            self.fp.flush()
        return ((self.lp[0]*0x10000+self.lp[1])*self.segmentsize
                +(os.stat("%s/segment-%04x/%04x.dat"%(self.filename,self.lp[0],self.lp[1]))[6]))
    def tell(self):
        return ((self.segment*0x10000+self.subsegment)*self.segmentsize)+self.fp.tell()
    def write(self,buffer):
        finishedwrite=False
        cpos=0
        while not finishedwrite:
            ip=self.fp.tell()
            lb=len(buffer)-cpos
            if (ip+lb>self.segmentsize):
                self.fp.write(buffer[cpos:cpos+(self.segmentsize-ip)])
                self.fp.close()
                self.subsegment+=1
                if (self.subsegment>=0x10000):
                    self.segment+=1
                    self.subsegment=0
                    assert(self.segment<0x10000)
                    os.mkdir("%s/segment-%04x"%(self.filename,self.segment))
                self.fp=open("%s/segment-%04x/%04x.dat"%(self.filename,self.segment,self.subsegment),self.mode)
                if (self.segment>=self.lp[0]):
                    if (self.subsegment>=self.lp[1]):
                        self.lp=(self.segment,self.subsegment)
                cpos+=(self.segmentsize-ip)
                lb=len(buffer)-cpos
                ip=0
            else:
                self.fp.write(buffer[cpos:])
                finishedwrite=True
    def read(self,amount=None):
        if (amount==None):
            raise Exception,"This kind of large file is not supposed to fit into your RAM"
        finishedread=False
        cpos=0
        res=""
        while not finishedread:
            ip=self.fp.tell()
            lb=amount-cpos
            if (ip+lb>self.segmentsize):
                res+=self.fp.read(self.segmentsize-ip)
                self.fp.close()
                self.subsegment+=1
                if (self.subsegment>=0x10000):
                    self.segment+=1
                    self.subsegment=0
                    assert(self.segment<0x10000)
                self.fp=open("%s/segment-%04x/%04x.dat"%(self.filename,self.segment,self.subsegment),self.mode)
                cpos+=(self.segmentsize-ip)
                lb=amount-cpos
                ip=0
            else:
                res+=self.fp.read(amount-cpos)
                finishedread=True
        return res
    def flush(self):
        self.fp.flush()
    def close(self):
        self.fp.close()
    def isatty(self):
        return False
    def filepointerdecoder(self): return strtouint64
    def filepointerencoder(self): return uint64tostr
    def filepointersize(self) : return 8
