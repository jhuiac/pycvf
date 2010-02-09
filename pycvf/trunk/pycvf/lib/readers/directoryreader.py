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
import Image
import os
import re
import itertools
import random
from pycvf.core.errors import pycvf_warning
from pycvf.lib.graphics.imgfmtutils import PIL2NumPy
from pycvf.lib.readers.corereader import CoreReader

class DirectoryReader:
    def __init__(self,path,filtere="(.*)",observer=None, randomized=True):
        self.filter=filter
        self.path=path
        ld=os.listdir(path)
        if (randomized):
          random.shuffle(ld)
        self.ld=ld
        self.observer=observer
        self.itername=itertools.imap( lambda x:os.path.join(self.path,x) ,itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld))
    def rewind(self):
        self.itername=itertools.imap( lambda x:os.path.join(self.path,x) ,itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld))
    def next(self):
        return self.itername.next()
    def step(self):
        i=self.next()
        if (self.observer):
            self.observer(i)
        return i
    def __iter__(self):
       try:
         while True:
            yield self.next()
       except KeyboardInterrupt:
           raise
       except Exception,e:
          pycvf_warning(str(e))
          pass
    def run(self):
        while True:
            self.step()


def ImgOpenOrNone(x):
  try:
    return PIL2NumPy(Image.open(x).convert("RGBA"))[:,:,:3]
  except:
    return None

class ImageDirectoryReader:
    def __init__(self,path,filtere="(.*).(jpg|png|gif|tif|tga|pgm|ppm)",observer=None, randomized=True):
        self.filter=filter
        self.path=path
        ld=os.listdir(path)
        if (randomized):
          random.shuffle(ld)
        else:
          ld.sort()
        self.ld=ld
        self.ca=None
        self.itername=itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld)
        self.iterimages=itertools.ifilter(lambda x:x!=None,itertools.imap(lambda x:ImgOpenOrNone(path+"/"+x),self.itername))
        self.iterimages_with_filenames=itertools.ifilter(lambda x:x[0]!=None,itertools.imap(lambda x:(ImgOpenOrNone(path+"/"+x),path+"/"+x) ,self.itername))
        self.observer=None
    def next(self):
        return self.iterimages_with_filenames.next()
    def step(self):
        i=self.next()
        if (self.observer):
            self.observer(i)
        return i
    def run(self):
        while True:
            self.step()
    def __getitem__(self,a):
        return ImgOpenOrNone(a)


class VideoDirectoryReader:
    def __init__(self,path,filtere="(.*).(avi|mpg|flv|mov)",observer=None, randomized=True):
        from pycvf.lib.video.simplevideoreader7 import SimpleVideoReader7
        self.filter=filter
        self.path=path
        ld=os.listdir(path)
        if (randomized):
          random.shuffle(ld)
        self.ld=ld
        self.itername=itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld)
        self.itervideos=itertools.imap(lambda x:SimpleVideoReader7(path+"/"+x),self.itername)
        self.itervideos_with_filenames=itertools.imap(lambda x:(SimpleVideoReader7(path+"/"+x),(path+"/"+x)) ,self.itername)
        self.observer=None
    def reset(self):
        if (randomized):
          random.shuffle(ld)
        self.ld=ld
        self.itername=itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld)
        self.itervideos=itertools.imap(lambda x:SimpleVideoReader7(path+"/"+x),self.itername)
        self.itervideos_with_filenames=itertools.imap(lambda x:(SimpleVideoReader7(path+"/"+x),(path+"/"+x)) ,self.itername)
        self.observer=None
    def next(self):
        return self.itervideos_with_filenames.next()
    def step(self):
        i=self.next()
        if (self.observer):
            self.observer(i)
        return i
    def run(self):
        while True:
            self.step()
            
            
class AudioDirectoryReader:
    def __init__(self,path,filtere="(.*).(wav|mp3|ogg)",observer=None, randomized=True):
        from pycvf.lib.video.simplevideoreader7 import SimpleVideoReader7
        self.filter=filter
        self.path=path
        ld=os.listdir(path)
        if (randomized):
          random.shuffle(ld)
        self.ld=ld
        self.itername=itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld)
        self.iteraudios=itertools.imap(lambda x:SimpleVideoReader7(path+"/"+x),self.itername)
        self.iteraudios_with_filenames=itertools.imap(lambda x:(SimpleVideoReader7(path+"/"+x),(path+"/"+x)) ,self.itername)
        self.observer=None
    def reset(self):
        if (randomized):
          random.shuffle(ld)
        self.ld=ld
        self.itername=itertools.ifilter(lambda x:re.match(filtere,x,re.I),ld)
        self.iteraudios=itertools.imap(lambda x:SimpleVideoReader7(path+"/"+x),self.itername)
        self.iteraudios_with_filenames=itertools.imap(lambda x:(SimpleVideoReader7(path+"/"+x),(path+"/"+x)) ,self.itername)
        self.observer=None
    def next(self):
        return self.iteraudios_with_filenames.next()
    def step(self):
        i=self.next()
        if (self.observer):
            self.observer(i)
        return i
    def run(self):
        while True:
            self.step()
