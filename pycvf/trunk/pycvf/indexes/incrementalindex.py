# -*- coding: utf-8 -*-
#import scipy.spatial
import numpy, pickle
from sashindex import SashIndex
from lshindex import LshIndex
from pycvf.core.errors import *

##
## Should we allow to pass iterators as database reference when creating an index ?
## (for the moment allowed types are list and arrays,  it is important to notify
## that most indexing structures require the data to keep existing in memory..
## thus very though data structure are devoter to off-core computing.
##

def unzipg(l):
  if (len(l)==0):
    yield 
  else:
    for i in range(len(l[0])):
      yield map(lambda x:x[i],l)

def unzip(l):
  r=[]
  if (len(l)==0):
    return [],[]
  else:
    for i in range(len(l[0])):
      r.append(map(lambda x:x[i],l))
    return tuple(r)


def concatiter(itators):
  for i in iterators:
     for e in i:
        yield e

def bruteforcenearest(possiblenearests, possiblenearestdistances,k):
    #if (len(possiblenearests))==0:
    #   return possiblenearests, possiblenearestdistances
    print possiblenearestdistances, possiblenearests
    dm=numpy.hstack(possiblenearestdistances).argsort(axis=0)
    print dm
    print numpy.vstack(possiblenearests)
    print numpy.vstack(possiblenearestdistances)
    r=map(lambda x:((x[0][0],x[0][1]),x[1][0]),zip(numpy.vstack(possiblenearests).take(dm[:k],axis=0),numpy.vstack(possiblenearestdistances).take(dm[:k],axis=0)))
    print "r=",r, "pn",possiblenearests
    return [r]


DefaultIndexClass=SashIndex

class IncrementalIndex:
  def __init__(self, filename=None,
                     BaseIndexClass=DefaultIndexClass, 
                     expected_elements_per_increment=256#-1
              ):
     self.BaseIndexClass=BaseIndexClass
     self.filename=filename
     self.idxcnt=0
     self.toadd=[]
     self.idxs=[]
     if (filename):
        pycvf_debug(10,"loading incremental indexfile "+ self.filename+".pcl")
        #d=pickle.load(self.filename+".pcl")      
        cont=True
        while cont:
          try:
            idx1=self.BaseIndexClass.load(self.filename+"-index%03d.idx"%(self.idxcnt,))
            pycvf_debug(10,"found indexfile "+ self.filename+"-index%03d.idx"%(self.idxcnt,))
            self.idxs.append(idx1)
            self.idxcnt+=1
          except Exception,e:
            pycvf_debug(10,"failed to load indexfile "+ self.filename+"-index%03d.idx"%(self.idxcnt,)+","+str(e))
            cont=False
            pass
      #if (idxcnt==0):

       # self.idxs=[]
     else:
        pycvf_debug(10,"no filename : no index loaded")
        self.idxs=[]
     self.smallsizethreshold=expected_elements_per_increment
     self.mink=int(numpy.floor(numpy.log2(self.smallsizethreshold)))

  def instantiate_new_idx(self):
     pycvf_debug(10,"instantiating new subindex "+self.filename+"-index%03d.idx"%(self.idxcnt,))
     try:
        idx1=self.BaseIndexClass(filename=self.filename+"-index%03d.idx"%(self.idxcnt,))
     except:
        idx1=self.BaseIndexClass()
     self.idxs.append(idx1)
     return idx1

  def add(self,key,value):
    #print "key",key,"value",value
    self.toadd.append([key,value])
    if (len(self.toadd)>self.smallsizethreshold):
       self.do_add()

  def add_many(self,keys,values):
     assert(type(keys) in [ list,numpy.ndarray ])
     #assert(type(keys)==type(values))
     ##
     if (type(keys)==list):
       nbelements=len(keys)
     else:
       nbelements=keys.shape[0]
     ##
     if (nbelements==0):
       return
     k=int(numpy.log2(nbelements))-self.mink
     k=max(k,0)
     self.add_many_to_bin(keys,values,k)


  #def

  def add_many_to_bin(self,keys,values,k):
     tidx=None
     while (tidx==None):
       try:
         tidx=self.idxs[k]
       except IndexError:
         self.instantiate_new_idx()
     ## We evaluate the size at which we will insert the data
  
     if ((len(tidx)+len(keys))>self.smallsizethreshold*(3**k)):
       ## we remove maxelems from the set that we pass upward
       self.add_many_to_bin(keys,values,k+1)
       if (self.idxs[k].keys()!=[]) :
         self.add_many_to_bin(numpy.array([x for x in self.idxs[k].keys()]), numpy.array([x for x in self.idxs[k].values()],dtype=object),k+1)
       self.idxs[k].reset()
     else:
       okeys=tidx.keys()
       ovalues=tidx.values() 
       tidx.reset()
       print okeys
       if (okeys!=[]):
         okk=numpy.array([ k for k in okeys])
         ovv=numpy.array([ v for v in ovalues])
         vva=numpy.array(values,dtype=object)
         kka=numpy.array(keys)
         kka=kka.reshape(kka.shape[0],-1)
         #print ovv
         print okk.shape, kka.shape, ovv.shape, vva.shape
         tidx.add_many(numpy.vstack([ okk,kka]),numpy.vstack([ovv,vva]))
         print len(tidx)
       else:
         tidx.add_many(keys,numpy.array(values,dtype=object))
         print len(tidx)

     ## Each bin may scale in between 0*k and 2.5*k, when it get a size greater than 3k then random elements among 2k are passed to the higher container...
     ##


  def getitems(self,x,n):
     pn=[]
     pnd=[]
     assert(len(self.idxs)>0)
     for i in self.idxs:
       n,nd=idxs.getitems(x,n)
       pn.extend(n)
       pnd.extend(nd)
     try:
       return bruteforcenearest(pn,pnd,n)
     except Exception,e:
       pycvf_warning("error computing brute force nearest for query")
       print pn
       print pnd
       return []  

  def query(self,values, *args ,**kwargs):
     return self.getitems( values, *args, **kwargs) 

  def __getitem__(self,query):
      if (len(self.toadd)):
         self.do_add()
      return self.getitem(query)
        
  def getitem(self,query,numelem=1):
     pn=[]
     pnd=[]
     if (len(self.toadd)>0):
         self.doadd(False)
     assert(len(self.idxs))
     for i in self.idxs: 
       pycvf_debug(10,"getitem")
       n,nd=unzip(i.getitems([query],numelem)[0])
       pn.extend(n)
       pnd.extend(nd)
     r=bruteforcenearest(pn,pnd,numelem)
     #print r
     return r

  def getitems(self,query,numelem=3):
     return self.getitem(query,numelem)

  def __del__(self):
      if (len(self.toadd)):
         self.do_add()

  def do_add(self,with_save=False):
     #print self.toadd
     #a=numpy.array(self.toadd)
     #pycvf_debug(10,"adding objects to index...")
     self.add_many(numpy.array(map(lambda x:x[0],self.toadd)),map(lambda x:x[1],self.toadd))
     self.toadd=[]
     if with_save:
       self.save()

  def save(self):
    if (len(self.toadd)):
       self.do_add()
    pycvf_debug(10,"saving index...len="+str(len(self.idxs)))
    c=0
    for i in self.idxs:
      pycvf_debug(10,"saving index..."+str(i))
      try:
        i.save()
      except:
        i.save(self.filename+"-index%03d.idx"%(c,))
      c+=1

  def keys(self):
      return concatiter(map(lambda x:x.keys(),self.idxs))
      
  def values(self):
      return concatiter(map(lambda x:x.values(),self.idxs))

  def __len__(self):
      return reduce(lambda x,y:x+len(y),self.idxs,len(self.toadd))
  @staticmethod
  def load(filename,BaseIndexClass=DefaultIndexClass):
      pycvf_debug(10,"trying to load index...")
      return IncrementalIndex(BaseIndexClass,filename)
      #r=[]
      #idxcnt=0
      #cont=True
      #while cont:
      #  try:
      #    idx1=self.BaseIndexClass.load(self.filename+"-index%03d.idx"%(idxcnt,))
      #    idxcnt+=1
      #  except:
      #    cont=False
      #    pass
      #if (idxcnt==0):
      #   raise Exception,"database not found => not loaded"
      
     
if __name__=="__main__":
  print "------------------------------------------------------------------------------------------------------------------------------"
  print "Testing Incremental Indexing #################################################################################################"
  print "------------------------------------------------------------------------------------------------------------------------------"
  idx=IncrementalIndex(baseclass=DefaultIndexClass)
  idx.add_many([x for x in range(200)],[x*x for x in range(200)])
  idx.save("toto.idx")
  del idx
  idx=GeneralIncrementalIndex(baseclass=DefaultIndexClass,filename="toto.idx")
  idx.add_many([200+x for x in range(200)],[x*x for x in range(200)])
  del idx
  #python ../../apps/build_index.py --db mvpimages --dbargs '' -m image.satohtest --value "@" --key "/" --idx incrementalindex
  #python pycvf/apps/gacbquery.py --db mvpimages --dbargs '' -m image.satohtest  --key "/" --idx incrementalindex

class ErasableDatabase:
   ## basically we maintain a container of the database of the removed elements
   ## when the size of this container becomes to big we rebuild the database
   pass


 
