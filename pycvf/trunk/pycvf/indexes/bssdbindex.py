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


import bsddb3
import cPickle as pickle
import itertools
import numpy
import scipy

class BssDbAny:
    def __init__(self,filename,dbname,protocol=2):
        self.db=bsddb3.db.DB()
        self.db.open(filename,dbname,dbtype=bsddb3.db.DB_BTREE, flags=bsddb3.db.DB_CREATE)
        self.protocol=protocol
    def __del__(self):
        self.db.close()
    def __getitem__(self,e):
        return pickle.loads(self.db[pickle.dumps(e,protocol=self.protocol)])#,protocol=self.protocol)
    def __setitem__(self,e,i):
        self.db[pickle.dumps(e,protocol=self.protocol)]=pickle.dumps(i,protocol=self.protocol)

class BssDbIScalar:
    def __init__(self,filename,dbname,savecmd=lambda x: pickle.dumps( x,protocol=2) , loadcmd=lambda x:pickle.loads(x)):
        self.db=bsddb3.db.DB()
        self.db.open(filename,dbname,dbtype=bsddb3.db.DB_BTREE, flags=bsddb3.db.DB_CREATE)
        self.loadcmd=loadcmd
        self.savecmd=savecmd
    def __del__(self):
        self.db.close()
    def __getitem__(self,e):
        return self.loadcmd(self.db["%024.8f"%(e)])#,protocol=self.protocol)
    def __setitem__(self,e,i):
        self.db["%024.8f"%(e)]=self.savecmd(i)
    def __getslice__(self,bmin,bmax):
        c=self.db.cursor()
        c.set_range("%024.8f"%(bmin))
        class xiter:
            def __init__(self,bmaxs,loadcmd):
                self.bmaxs=bmaxs
                self.loadcmd=loadcmd
            def __iter__(self):
                return self.next()
            def next(self):
                while True:
                    t=c.current()
                    yield self.loadcmd(t[1])
                    c.next()
                    if (c.current()[0]>self.bmaxs):
                        break
        return xiter(bmax,self.loadcmd).__iter__()
        #return ifilter(lambda x:pickle.loads(x,protocol=self.protocol),)
    def add(self,e,i):
        try:
            self[e]=(self[e] or []) + [i]
        except:
            self[e]=[i]



class BssDbIString:
    def __init__(self,filename,dbname,protocol=2, encoding='utf8'):
        self.db=bsddb3.db.DB()
        self.db.open(filename,dbname,dbtype=bsddb3.db.DB_BTREE, flags=bsddb3.db.DB_CREATE)
        self.protocol=protocol
        self.encoding=encoding
    def __del__(self):
        self.db.close()
    def __getitem__(self,e):
        if (type(e)==unicode):
            e=e.encode(self.encoding)
        return pickle.loads(self.db[e])#,protocol=self.protocol)
    def __setitem__(self,e,i):
        if (type(e)==unicode):
            e=e.encode(self.encoding)
        self.db[e]=pickle.dumps(i,protocol=self.protocol)
    def add(self,e,i):
        if (type(e)==unicode):
            e=e.encode(self.encoding)
        try:
            self[e]=(self[e] or []) + [i]
        except:
            self[e]=[i]

def encstr(s):
    ls="%08x"%(len(s))
    return str(ls)+s

def decstrlst(s):
    ne=int(s[0:8],16)
    be=8
    r=[]
    for e in range(ne):
        l=int(s[be:be+8],16)
        x=s[be+8:be+8+l]
        r.append(numpy.ndarray(buffer=buffer(x),shape=(l/4), dtype=numpy.float32))
        be+=(8+l)
    return r

class MultidimensionalDb:
    def __init__(self, filebase, dbname,nd):
        self.nd=nd
        self.idx=BssDbIString(filebase+".db",dbname+"_base")
        self.addidxaxr=numpy.zeros((nd,),dtype=object)
        for i in range(nd):
            self.addidxaxr[i]=BssDbIScalar(filebase+"-"+str(i)+".idx",
                                           dbname+"_idx"+str(i),
                                           savecmd=lambda x:reduce(lambda y,z:y+encstr(z.astype(numpy.float32).tostring()),x,("%08x"%(len (x)))),
                                           loadcmd=lambda x:decstrlst(x)
                                           )
    def add(self,key,reference):
        #print key,reference
        key=numpy.array(key).astype(numpy.float32)
        self.idx.add(key.tostring(),reference)
        for d in range(len(self.addidxaxr)):
            self.addidxaxr[d].add(key[d],key)
    def __getitem__(self,key):
        return self.idx[numpy.array(key).astype(numpy.float32).tostring()]
    def get_clipping_box(self,key,radius):
        minbounds=key-radius
        maxbounds=key+radius
        return minbounds, maxbounds
    def __getball__(self,key,radius):
        minbounds,maxbounds=self.get_clipping_box(key,radius)
        ia=self.addidxaxr[0]
        sbi=minbounds[0]
        bbi=maxbounds[0]
        xi=reduce(lambda x,y:x+y,ia[sbi:bbi],[])
        xi=filter(lambda x:((sbi<x).all() and (x<bbi).all()) ,xi)
        xi=map(lambda x:self[x],xi)
        #scipy.unique(xi)
        #for i in range(1,len(self.addidxaxr)):
        #    ia=self.addidxaxr[i]
        #    sbi=minbounds[i]
        #    bbi=maxbounds[i]
        #    #xi2=set(reduce(lambda x,y:x+filter(lambda x: x.numpy.array(y)),ia.__getslice__(sbi,bbi),[]))
        #    xi.intersection_update(xi2)
        return xi

#mdb=MultidimensionalDb("/tmp/mdbx","mdb",3)
#mdb.add(numpy.array([3,2,1]),"toto")
