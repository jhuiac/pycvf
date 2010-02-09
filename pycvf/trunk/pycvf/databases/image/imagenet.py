# -*- coding: utf-8 -*-
import urllib,os

from pycvf.core import settings
if not os.environ.has_key("WNHOME"):
   os.environ["WNHOME"]=settings.WNHOME
if not os.environ.has_key("WNDICT"):
   os.environ["WNDICT"]=settings.WNDICT

from pycvf.core.errors import *
from pycvf.lib.ontology.pywn import stdwn 
from pycvf.lib.graphics.rescale import Rescaler2d
from pycvf.lib.graphics.imgfmtutils import PIL2NumPy
from pycvf.datatypes import image as image
from pycvf.core import database
from pycvf.lib.misc.multidownload import MultiDownloader

from PIL import Image


class ImageNet:
    """ This class implements the  ImageNet API"""
    @staticmethod 
    def solvequery(word,interactive=True):
        if word[0]=="#":
          return word[1:].split('(')[0]
        r=stdwn.impl.lookupSynsetsByForm(word)
        if (len(r)==0):
          raise KeyError, "No Element Matching that query"
        nr=filter(lambda x:x.key[0]==0,r)
        if (len(nr)==0):
           pycvf_debug(20,str(( word, r)))
           raise Exception, "Verbs, Adjectives are not yet supported by ImageNet"
        if (len(nr)>1):
          if (interactive==True):
            cont=True
            while cont:
              for r in zip(range(len(nr)),nr):
                print(r)
              try: 
                print "your choice :"
                r=nr[int(sys.stdin.readline())]
                cont=False
                print dir(r)
                pycvf_warning("to avoid interaction use following reference later "+("#n%08d(%s)"%(r.key[1],r)))
              except KeyboardInterrupt: 
                raise
              except:
                pass
          else:
            pycvf_warning("The word "+w+" is ambiguous")
            pycvf_warning("default set to first meaning")
            r=nr[0]
        else:
          r=nr[0]
        r=r.key
        return ("n%08d"%(r[1],))

    @staticmethod
    def page(query):
        import BeautifulSoup
        wnid=ImageNet.solvequery(query)
        url="http://www.image-net.org/synset?wnid=%s"%(wnid,)
        return BeautifulSoup.BeautifulSoup(urllib.urlopen(url).read())
    @staticmethod
    def hyponyms(query,full=False):
        wnid=ImageNet.solvequery(query)
        url="http://www.image-net.org/api/text/wordnet.structure.hyponym?wnid=%s"%(wnid,)
        if (full):
            url+="&full=1"
        return urllib.urlopen(url).read()
    @staticmethod
    def synset(query):
        wnid=ImageNet.solvequery(query)
        url="http://www.image-net.org/api/text/wordnet.synset.getwords?wnid=%s"%(wnid,)
        return urllib.urlopen(url).read()
    @staticmethod
    def urls(query,limit=40):
        wnid=ImageNet.solvequery(query)
        url="http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=%s"%(wnid,)
        return filter(lambda x:(len(x)>0),map(lambda x:x.strip(),urllib.urlopen(url).read().split("\n")))[:limit]



class DB(database.ContentsDatabase,image.Datatype):
  def __init__(self,query="factory", limit=40,with_cache=None,rescale=(300,400,'T')):
    done=False
    self.rescale=rescale
    if (with_cache):
      try:
         os.stat(with_cache+"/"+query.lower())
         f=file(with_cache+"/"+query+"/reader.pcl","rb")
         self.query=pickle.load(f)
         self.urls=pickle.load(f)
         self.destdir=pickle.load(f)
         self.lq=pickle.load(f)
         done=True
      except: 
         pass
    if not done:    
      self.query=query
      self.urls=ImageNet.urls(query,limit)
      pycvf_debug(10,str(self.urls))
      if not (with_cache):
        self.destdir="/tmp/"+query.lower()
      else:
        self.destdir=with_cache+yahoo_image_search.query.lower()
      try:
        os.mkdir(self.destdir)
      except:
        pass
      self.lq=len(self.urls)
      dl=map(lambda i:(self.urls[i],(self.destdir+"/f-"+str(i)+"."+self.urls[i].split(".")[-1]).lower()) ,range(len(self.urls)))
      if (self.lq):
        md=MultiDownloader(dl)
        md.run()
    if (with_cache):
      try:
        os.mkdir(with_cache+"/"+query.lower())
      except:
        pass
      f=file(with_cache+"/"+query+"/reader.pcl","wb")
      pickle.dump(self.query,f,protocol=2)
      pickle.dump(self.urls,f,protocol=2)
      pickle.dump(self.destdir,f,protocol=2)
      pickle.dump(self.lq,f,protocol=2)
      f.close()
  def __iter__(self):
     for i in range(self.lq):
        try:
          fname=(self.destdir+"/f-"+str(i)+"."+self.urls[i].split(".")[-1]).lower()
          #print "opening "+fname
          img=Image.open(fname)
          if (self.rescale!=None):
            rescale=Rescaler2d(self.rescale).process
          else:
            rescale=lambda x:x
          yield (rescale(PIL2NumPy(img)),(self.query,i))
        except (IOError,ValueError):
          pycvf_warning( "ERROR loading image " + str(i) +" of " + str(self.lq))
          pass
  def __getitem__(self,i):
          assert(i[0]==self.query)
          i=i[1]
          fname=(self.destdir+"/f-"+str(i)+"."+self.urls[i].split(".")[-1]).lower()
          #print "opening "+fname
          img=Image.open(fname)
          if (self.rescale!=None):
            rescale=Rescaler2d(self.rescale).process
          else:
            rescale=lambda x:x
          return rescale(PIL2NumPy(img))

ContentsDatabase=DB
__call__=DB