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
import cPickle as pickle
import numpy
import ctypes
import os,zlib

from pycvf.core.errors import *
from pycvf.core.builders import *

def check_has_title(mo):
    try:
        assert(mo["title"])
        return True
    except:
        return False

## A track that does not keep track of anything ....
class NullTrack(object):
    def __init__(self,meta=None):
        self.metafilter=map(check_has_title,meta)
        self.meta=meta
        pass
    def savemeta(self):
        pass
    def saveindex(self):
        pass
    def rewind(self):
        pass
    def __iter__(self):
        return self
    def makeindex(self):
        pass
    def __getitem__(self,no):
        raise KeyError
    def next(self):
        raise StopIteration
    def append(self,o):
        pass


class OnDiskTrack(object):
    def __openfiler(self):
        if (self.mode!='rb+'):
            if (self.fp): self.fp.close()
            self.mode='rb+'
            self.fp=open(self.filename,self.mode)
            self.fplen=os.stat(self.filename).st_size            
    def __openfilea(self):
        if (self.mode!='ab+'):
            if (self.fp): self.fp.close()
            self.mode='ab+'
            self.fp=open(self.filename,self.mode)
            self.fplen=os.stat(self.filename).st_size                        
    def __init__(self,filename,saverate=10,meta=None):
        self.filename=filename
        self.mode=''
        self.fp=None
        self.fplen=0
        self.ano=0
        self.tryloadmeta()
        if (meta!=None):
            self.metafilter=map(check_has_title,meta)
            #assert(True in self.metafilter)
            self.meta=meta
        self.tryloadindex()
        self.saverate=saverate
    def __del__(self):
        self.saveindex()
        self.savemeta()
    def savemeta(self):
        if (self.meta!=None):
            metaf=file(("%s.meta"%(self.filename)),"w")
            print "meta"
            pickle.dump(self.meta,metaf)
            print "/meta"
            metaf.close()
    def saveindex(self):
        if (self.index!=None):
            indexf=file(("%s.idx"%(self.filename)),"w")
            pickle.dump(self.index,indexf)
            indexf.close()
    def __len__(self):
        if (not self.index):
            self.makeindex()
        return len(self.index)
    def rewind(self):
        self.fp=None
        self.mode=''
    def __iter__(self):
        return self
    def tryloadmeta(self):
        try:
            filename=("%s.meta"%(self.filename))
            metaf=open(filename,"r")
            try:
              self.meta=pickle.load(metaf)
            except:
              self.meta=pycvf_pickle_loader(filename)
            self.metafilter=map(check_has_title,self.meta)
            metaf.close()
        except Exception,e:
            # print "Exception occured in loading metadata :"+str(e)
            self.meta=None
            self.metafilter=None
    def tryloadindex(self):
        try:
            indexf=open(("%s.idx"%(self.filename)),"r")
            self.index=pickle.load(indexf)
            indexf.close()
        except:
            self.index=[]
    def makeindex(self):
        self.__openfiler()
        cp=self.fp.tell()
        self.index=[]
        try:
            while self.next():
                self.index.append(cp)
                cp=self.fp.tell()
        except:
            pass
    def __getitem__(self,no):
        if (not self.index):
            self.tryloadindex()
            if (not self.index):
                self.makeindex()
        self.__openfiler()
        offset=self.index[no]
        self.fp.seek(offset)
        return self.next()
    def _internalread(self):
        return pickle.load(self.fp)
    def _internalwrite(self,o):
        pickle.dump(o,self.fp)
    def next(self):
        try :
            self.__openfiler()
            return self._internalread()
        except:
            raise StopIteration
    def append(self,o):
        self.__openfilea()
        self.index.append( self.fp.tell() )
        self._internalwrite(o)
        self.ano+=1
        if (self.ano%self.saverate==0):
            self.fp.flush()




## avoid reading all subtracks when only one is needed
class _OnDiskMultiTrack(object):
    def _internalread(self):
        class LazyLoader:
            def __init__(self,fp,ofa):
                self.fp=fp
                self.ofa=ofa
            def __getitem__(self,no):
                self.fp.seek(self.ofa[no])
                return pickle.load(self.fp)
            def __len__(self):
                return len(self.ofa)
        leno=self.fp.read(4)
        leno=(ctypes.cast(ctypes.c_char_p(leno),ctypes.POINTER(ctypes.c_int32))).contents.value
        rbuff=self.fp.read(4*(leno+1))
        ofa=[]
        for i in range(leno):
            ofa.append((ctypes.cast(ctypes.c_char_p(rbuff[4*i:4*(i+1)]),ctypes.POINTER(ctypes.c_int32))).contents.value)
        next=(ctypes.cast(ctypes.c_char_p(rbuff[4*leno:4*(leno+1)]),ctypes.POINTER(ctypes.c_int32))).contents.value
        self.fp.seek(next)
        return LazyLoader(self.fp,ofa)
    def _internalwrite(self,o):
        cp=self.fp.tell()
        l=len(o)
        self.fp.write(ctypes.string_at(ctypes.pointer(ctypes.c_int32(l)),4))
        assert(self.metafilter)
        assert(l==len(self.metafilter))
        ds=[]
        for i in range(l):
            if self.metafilter[i]:
              ds.append(pickle.dumps(o[i]))
            else:
              ds.append(pickle.dumps(None))
        ofa=numpy.array([0]+map(len,ds),dtype=numpy.uint32).cumsum()# compute offsets
        ofa+=(cp+((2+l)*4)) # relocate correctly
        for off in ofa:
            self.fp.write(ctypes.string_at(ctypes.pointer(ctypes.c_int32(off)),4))
        for i in range(len(ds)):
            if (self.fp.tell()!=ofa[i]):
                raise Exception, ("error file @ %d but declared offset at %d"%(self.fp.tell(),ofa[i]))
            self.fp.write(ds[i])


## avoid reading all subtracks when only one is needed
class _OnDiskMultiTrackZ(object):
    def _internalread(self):
        class LazyLoader:
            def __init__(self,fp,ofa,iscompress):
                self.fp=fp
                self.ofa=ofa
                self.iscompress=iscompress
            def __getitem__(self,no):
                #print no, len(self), self.ofa
                self.fp.seek(self.ofa[no])
                if (self.iscompress[no]):
                    leno=self.fp.read(4)
                    leno=(ctypes.cast(ctypes.c_char_p(leno),ctypes.POINTER(ctypes.c_int32))).contents.value
                    buff=self.fp.read(leno)
                    return pickle.loads(zlib.decompress(buff))
                else:
                    return pickle.load(self.fp)
            def __len__(self):
                return len(self.ofa)
        leno=self.fp.read(4)
        leno=(ctypes.cast(ctypes.c_char_p(leno),ctypes.POINTER(ctypes.c_int32))).contents.value
        rbuff=self.fp.read(4*(leno+leno+1))
        ofa=[]
        iscompress=[]
        for i in range(leno):
            ofa.append((ctypes.cast(ctypes.c_char_p(rbuff[(8*i):(8*i+4)]),ctypes.POINTER(ctypes.c_int32))).contents.value)
            iscompress.append((ctypes.cast(ctypes.c_char_p(rbuff[(8*i+4):(8*i+8)]),ctypes.POINTER(ctypes.c_int32))).contents.value)
        next=(ctypes.cast(ctypes.c_char_p(rbuff[(8*leno):(8*leno+4)]),ctypes.POINTER(ctypes.c_int32))).contents.value
        self.fp.seek(next)
        return LazyLoader(self.fp,ofa,iscompress)
    def _internalwrite(self,o):
        cp=self.fp.tell()
        l=len(o)
        self.fp.write(ctypes.string_at(ctypes.pointer(ctypes.c_int32(l)),4))
        ds=[pickle.dumps(so) for so in o]
        ls=map(len,ds)
        iscompress=[0]*l
        for i in range(l):
            if (ls[i]>64):
                ds[i]=zlib.compress(ds[i])
                ls[i]=len(ds[i])
                clen=ctypes.string_at(ctypes.pointer(ctypes.c_int32(ls[i])),4)
                ds[i]=clen+ds[i]
                ls[i]+=4
                iscompress[i]=1
        ofa=numpy.array([0]+ls,dtype=numpy.uint32).cumsum()# compute offsets
        ofa+=(cp+((2+l+l)*4)) # relocate correctly
        for i in range(l):
            self.fp.write(ctypes.string_at(ctypes.pointer(ctypes.c_int32(ofa[i])),4))
            self.fp.write(ctypes.string_at(ctypes.pointer(ctypes.c_int32(iscompress[i])),4))
        self.fp.write(ctypes.string_at(ctypes.pointer(ctypes.c_int32(ofa[l])),4)) # write next block
        for i in range(len(ds)):
            if (self.fp.tell()!=ofa[i]):
                raise Exception, ("error file @ %d but declared offset at %d"%(self.fp.tell(),ofa[i]))
            self.fp.write(ds[i])


class OnDiskMultiTrack(_OnDiskMultiTrack,OnDiskTrack):
    pass

class OnDiskMultiTrackZ(_OnDiskMultiTrackZ,OnDiskTrack):
    pass


## this version uses multiple files to avoid having to enable large file support in python
## a bit cucumbersome
class OnDiskTrackLarge(OnDiskTrack):
    def __openfiler(self):
        if (self.mode!='rb+'):
            if (self.fp): self.fp.close()
            self.mode='rb+'
            self.cfileno=0
            self.fp=open(("%s-%04d.mfa"%(self.filename,self.cfileno)),self.mode)
            self.fplen=os.stat(("%s-%04d.mfa"%(self.filename,self.cfileno))).st_size            
    def __openfilea(self):
        if ((self.mode!='ab+') or (self.fp.tell() > 0x70000000)):
            self.cfileno=self.next_free_file();
            if (self.fp): self.fp.close()
            self.mode='ab+'
            self.fp=open(("%s-%04d.mfa"%(self.filename,self.cfileno)),self.mode)
            self.fplen=os.stat(("%s-%04d.mfa"%(self.filename,self.cfileno))).st_size                        
    def __init__(self,*args,**xargs):
        super(OnDiskTrackLarge,self).__init__(*args,**xargs)
        self.cfileno=-1
    def next_free_file(self):
        testno=-1
        found=True
        while found:
            testno=testno+1
            try:
                os.stat(("%s-%04d.mfa"%(self.filename,testno)))
            except:
                found=False
            return testno
    def rewind(self):
        super(OnDiskTrackLarge,self).rewind()
        self.cfileno=-1
    def next(self):
        try :
            self.__openfiler()
            if (self.fp.tell()==self.fplen):
                #print  "FPLEN=",self.fplen
                raise StopIteration
            return self._internalread()
        except Exception,e:
            #print "ex=",e
            try:
                (os.stat(("%s-%04d.mfa"%(self.filename,self.cfileno+1))))
            except:
                
                raise StopIteration
            self.fp.close()
            self.cfileno+=1
            self.fp=gzip.open(("%s-%04d.mfa"%(self.filename,self.cfileno)),self.mode)
            print dir(self.fp)
            self.fplen=os.stat(("%s-%04d.mfa"%(self.filename,self.cfileno))).st_size
            return self._internalread()
    def append(self,o):
        self.__openfilea()
        self.index.append((self.cfileno,self.fp.tell()))
        self._internalwrite(o)
        self.ano+=1
        if (self.ano%self.saverate==0):
            self.fp.flush()
    def makeindex(self):
        pycvf_warning( "remaking index... this operation may be long !!!")
        self.index=[]
        self.rewind()
        self.__openfiler()
        cp=(self.cfileno,self.fp.tell())
        c=0
        try:
            while self.next():
                sys.stderr.write("reading record (%d,%d,%d)\r"%(c,self.cfileno,self.fp.tell()))                
                self.index.append(cp)
                cp=(self.cfileno,self.fp.tell())
                c+=1
        except StopIteration:
            sys.stderr.write("\nindexing done\n")
            pass            
    def __getitem__(self,no):
        if (not self.index):
            self.makeindex()
        self.__openfiler()
        xfileno,offset=self.index[no]
        if (xfileno!=self.cfileno):
            self.fp=file(("%s-%04d.mfa"%(self.filename,self.cfileno)),self.mode)
            self.cfileno=xfileno
        self.fp.seek(offset)
        return self.next()



class OnDiskMultiTrackLarge(_OnDiskMultiTrack,OnDiskTrackLarge):
    pass

class OnDiskMultiTrackLargeZ(_OnDiskMultiTrackZ,OnDiskTrackLarge):
    pass

#class OnDiskMultiTrackLarge(OnDiskTrackLarge):
#    def __init__(self,*args,**xargs):
#        super(OnDiskMultiTrackLarge,self).__init__(*args,**xargs)
#        self._internalread=OnDiskMultiTrack._internalread
#        self._internalwrite=OnDiskMultiTrack._internalwrite
#
#class OnDiskMultiTrackLargeZ(OnDiskTrackLarge):
#    def __init__(self,*args,**xargs):
#        super(OnDiskMultiTrackLargeZ,self).__init__(*args,**xargs)
#        self._internalread=OnDiskMultiTrackZ._internalread
#        self._internalwrite=OnDiskMultiTrackZ._internalwrite
