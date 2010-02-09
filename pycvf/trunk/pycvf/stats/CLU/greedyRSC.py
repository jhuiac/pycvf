# -*- coding: utf-8 -*-
import os, numpy
from pycvf.core.utilities import *

GREEDYRSC_PATH=pycvf_var("GREEDYRSC_PATH",os.path.join(os.path.dirname(__file__),"greedyRSC"))
GREEDYRSC_PROGRAM=pycvf_var("GREEDYRSC_PROGRAM","GreedyRSC")

def length(x):
  if (type(x) in [numpy.ndarray]):
    return x.shape[0]
  else: 
    return len(x)

def write_annfile(filename,dbreader):
      f=file(filename,"w")
      f.write("%d\n"%(length(dbreader),))
      for i in dbreader:
          f.write("%s\n"%(str(i),))

def write_dvffile(filename, dbreader):
     f=file(filename,"w")
     f.write("%d\n"%(length(dbreader),))
     for i in dbreader:
          f.write('%d %s'%(i.shape[-1] ,' '.join(map(str,i.flat))+"\n"))


def decode_cldline(l):
  fp=["id","base_data_item","cluster_size","cluster_size+fringe","sampling_level","neighborhood_pattern_size", "size_sample","self_confidence", "zstat", "adjacent_clusters"]
  fpt=[int, int, int, int, int, int , int, float, float, int ]
  d=dict(zip(fp,l[:len(fp)]) )
  rl=l[len(fp):]
  for i in range(int(d['adjacent_clusters'])):
    d["id-a%d"%(i,)],d["c-a%d"%(i,)]=rl[i*2,i*2+1]
  return d

def read_clustercld(filename):
    f=file(filename)
    ln="%"
    while (len(ln)<1) or (ln[0]=="%"):
      ln=f.readline()
    nl=int(ln.split(' ')[0])
    lns=f.readlines()
    #assert(len(lns)==nl)
    return map(decode_cldline,filter(lambda ln:(len(ln)>1),map(lambda ln:map(float,ln.split(' ')),lns)))


def read_clustermem(filename):
    f=file(filename)
    ln="%"
    while (len(ln)<1) or (ln[0]=="%"):
      ln=f.readline()
    nl=int(ln.split(' ')[0])
    lns=f.readlines()
    assert(len(lns)==nl)
    return map(lambda x:numpy.array(x[1:]).reshape((len(x)-1)/2,2) ,filter(lambda ln:(len(ln)>1),map(lambda ln:map(float,ln.split(' ')[1:]),lns)))    

    

def read_clusterimem(filename):
    f=file(filename)
    ln="%"
    while (len(ln)<1) or (ln[0]=="%"):
      ln=f.readline()
    nl=int(ln.split(' ')[0])
    lns=f.readlines()
    assert(len(lns)==nl)
    return map(lambda x:numpy.array(x[1:]).reshape((len(x)-1)/2,2) ,filter(lambda ln:(len(ln)>1),map(lambda ln:map(int,ln.split(' ')[1:]),lns)))


def trymkdir(dirname):
  try:
    os.mkdir(dirname,0777)
  except OSError:
    pass
  os.stat(dirname)

class GreedyRSC(object):
  default_options={
       'cstyle':'hard+dist',
       'tload':'none',
       'tsave':'all',
       'cload':'none',
       'csave':'all',
       'view':'all',
       'eval':'all',
       'vformat':'image',
       'sashdeg':4,
       'nnacc':1.0,
       'mdir':"file:///D:/Documents and Settings/Mike/My Documents/data/aloi/members"
     }

  def __init__(self,datadirectory,dbname=None,views=True):
    self.datadirectory=datadirectory
    if (dbname==None):
      self.dbname=os.path.basename(self.datadirectory)
    self.options=self.default_options.copy()
    self.options['idir']=os.path.join(self.datadirectory,"input")
    self.options['tdir']=os.path.join(self.datadirectory,"temp")
    self.options['cdir']=os.path.join(self.datadirectory,"clusters")
    self.options['vdir']=os.path.join(self.datadirectory,"views")
    if views==False:
      self.options['view']='none'
      self.options['eval']='none'
      del self.options['vformat']
      del self.options['mdir']
  def prepare_datadir(self,removeifexists=True):
     if (removeifexists):
       os.system("rm -rf "+self.datadirectory)
     trymkdir(self.datadirectory)
     trymkdir(self.options['cdir'])
     trymkdir(self.options['idir'])
     trymkdir(self.options['tdir'])
     trymkdir(self.options['vdir'])
     optionfile=file(os.path.join(self.datadirectory,"options.txt"),"w")
     for i in self.options.items():
        optionfile.write("%s=%s\n"%(i[0],str(i[1])))
  def prepare_data_normal(self,data_reader, ground_truth_classification_reader=None, annotation_reader=None):
      write_dvffile(os.path.join(self.options['idir'],"%s.dvf"%(self.dbname,)) ,data_reader)
      if (ground_truth_classification_reader!=None):
        write_annfile(os.path.join(self.options['idir'],"%s_class.ann"%(self.dbname,)) ,ground_truth_classification_reader)
      if (annotation_reader!=None):
        write_annfile(os.path.join(self.options['idir'],"%s_annot.ann"%(self.dbname,)) ,annotation_reader)
  def prepare_data_large(self,data_reader, ground_truth_classification_reader=None, annotation_reader=None):
      write_dvffile(os.path.join(self.options['idir'],"%s_c0-b0.dvf"%(self.dbname,)) ,data_reader)
      if (ground_truth_classification_reader!=None):
        write_annfile(os.path.join(self.options['idir'],"%s_class_c0-b0.ann"%(self.dbname,)) ,ground_truth_classification_reader)
      if (annotation_reader!=None):
        write_annfile(os.path.join(self.options['idir'],"%s_annot_c0-b0.ann"%(self.dbname,)) ,annotation_reader)
  def do_compute(self):
     f=os.fork()
     if (f!=0):
       os.wait()
     else:
       os.execv(os.path.join(GREEDYRSC_PATH,GREEDYRSC_PROGRAM),
              [GREEDYRSC_PROGRAM,self.dbname+".dvf",os.path.join(self.datadirectory,"options.txt") ] 
             )
  def compute(self,data_reader, ground_truth_classification_reader=None, annotation_reader=None):
     self.prepare_datadir()
     self.prepare_data_large(data_reader, ground_truth_classification_reader, annotation_reader)
     self.do_compute()
  def read_cluster(self, method=None):
     if (method==None):
        method=self.options[cstyle]
     return read_clustermem(os.path.join(self.options['cdir'],"%s_%s_c0-b0.mem"%(self.dbname,method)))
  def read_cld(self):
     if (method==None):
        method=self.options[cstyle]      
     return read_clustercld(os.path.join(self.options['cdir'],"%s_%s_c0-b0.cld"%(self.dbname,method)))
  def cluster(self,*args,**kwargs):
    g.compute(data, ground_truth_classification_reader=map(str,gtdata), annotation_reader=map(str, data))
    return g.read_cluster('hard+dist')

 
 
 

 
 
 
 
 
 
 
 
 
 
 
############################################################################
 
def udist(npoints, center, radius):
   """ generate npoints from uniform distribution within a cube centered on center with radius radius """
   return ((numpy.random.random((npoints,len(center)))-0.5)*radius+numpy.array(center))

def gdist(npoints, center, radius):
   """ generate npoints from gaussian distribution centered on center with radius radius """
   return numpy.random.normal(center,radius,(npoints,len(center)))



if __name__=="__main__":
  import pylab
  pylab.ion()
  pylab.figure()
  ## neighborhood side 60
  ## a cluster should not  be larger than 1/5...
  import random
  numpy.random.seed(1)
  random.seed(1)
  print "Testing greedyRSC"
  g=GreedyRSC("simpletest",views=False)
  g.options['view']='all'
  g.options['vformat']='text'
  g.options['lists']='large'
  #g.options['nnacc']='exact'
  res=[]
  for ne in range(4,10):
    NE=(ne**3)+60
    sigma=0.0012
    adata=[gdist(NE,(random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50)),sigma) for i in range(50)]
    data=numpy.vstack(adata) #, gdist(NE//3,(4,3,5,1),0.02)])
    for c in adata:
       print c.mean(axis=0), c.std(axis=0)
    gtdata=reduce(lambda x,y:x+[y]*NE ,range(10),[])
    pylab.clf()
    #print data
    g.compute(data, ground_truth_classification_reader=map(str,gtdata), annotation_reader=map(str, data))
    clstr=g.read_cluster('hard+dist')
    cltrcolor=numpy.zeros((data.shape[0],4),dtype=numpy.float)
    for ci in range(len(clstr)):
       print clstr[ci][:,0].astype(int)
       cltrcolor[clstr[ci][:,0].astype(int),:]=(pylab.cm.hsv(float(ci)/len(clstr))[:4])
       #print cltrcolor[clstr[ci][:,0].astype(int),:]
    pylab.scatter(data[:,0],data[:,1],c=cltrcolor)#,marker='+')
    pylab.savefig("cluster-hard+dist-pts-%d.png"%(NE))
    pylab.show()
    print  clstr
    res.append(len(clstr))
  print "res,", res
  #print g.read_cld()
  #from pycvf
