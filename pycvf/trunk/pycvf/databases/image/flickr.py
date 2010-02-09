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
import os
from pycvf.lib.misc.multidownload import MultiDownloader
from pycvf.lib.graphics.rescale import Rescaler2d
from pycvf.lib.graphics.imgfmtutils import PIL2NumPy
from pycvf.datatypes import image as image
from pycvf.core import database
import pickle
from PIL import Image

class DB(database.ContentsDatabase):
  def datatype(self):
      return image.Datatype
  def __init__(self,query="Rocket",results=50, with_cache=None,rescale=None):
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
      from pycvf.lib.ontology.yim import yahoo_image_search
      yahoo_image_search.query = query
      yahoo_image_search.results = results
      r=yahoo_image_search.get_results()
      self.query=query
      self.urls=[ ]
      for i in range(40):
         try:
            self.urls.append(r.childNodes[0].getElementsByTagName('Result')[i].getElementsByTagName('Url')[0].childNodes[0].nodeValue)
         except:
            pass
      if not (with_cache):
        self.destdir="/tmp/"+yahoo_image_search.query.lower()
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
          print "ERROR loading image " + str(i) +" of " + str(self.lq)
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

# Framework 2 compatibility
ContentsDatabase=DB
__call__=DB