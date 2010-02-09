#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pycvf.core.version import version
import dialog

print "Python Computer Vision Framework v."+str(version)

from pycvf.core.directories import *

def download(url,filename,progressindicator=None):
    import urllib
    h=urllib.urlopen(url)
    f=file(filename,"wb")
    toberead=h.info()['content-length']
    p=0
    if (progressindicator):
      progressindicator(100*float(p)/float(toberead))
    while (p!=toberead):
       r=h.read(65536)
       f.write(r)
       p+=len(r)
       if (progressindicator):
         progressindicator(100*float(p)/float(toberead)) 
    f.close()

def untar(filename):
    os.system("tar -xvf "+filename)

def untargz(filename):
    os.system("tar -xvzf "+filename)

def untarbz2(filename):
    os.system("bzip2 -cd %s | tar -xv "%(filename,))
    
def ungz(filename):
    os.system("gunzip "+filename)

def unzip(filename):
    os.system("unzip "+filename)

Mb=1024*1024
Gb=1024*Mb

databases=[]

curdir=os.getcwd()
p=os.path.dirname(__file__)

if p:
  os.chdir(p)

os.chdir("databases")
for x in filter(lambda x:unicode(x[-3:])==u".py",os.listdir(".")):
   databases+=eval(file(x).read())
os.chdir(curdir)



def humansize(sz):
  if (sz==-1):
    return ""
  elif (sz<(1024*10)):
    return str(sz)+" bytes"
  elif (sz<(10*1024**2)):
    return str(sz//1024)+" Kb"
  elif (sz<(10*1024**3)):
    return str(sz//(1024**2))+" Mb"
  elif (sz<(10*1024**4)):
    return str(sz//(1024**3))+" Gb"
  else:
    return str(sz//(1024**4))+" Tb"


PYCVF_DATABASE_DIR


def main():
  d=dialog.Dialog()

  res=d.msgbox("""
  Welcome to PYCVF (version %s) database installation program
  ================================================================ 
    
  This program aims at providing you an easy way to get initial datas for your experimentations.
  
  
  This program will download many database and install them into : %s.
  
  If this location is not suitable for your please quit this program, edit your configuration file
  and sett the value PYCVF_DATABASE_DIR, and rerun this program. 
  
  """%(str(version),PYCVF_DATABASE_DIR),30,70)
  if res!=0:
    sys.exit(-1)

  res=d.checklist('Select the databases that you want to install', 
                  width=80, 
                  choices=[ (str(cd[1]),cd[0][1]['title']+ " " +humansize(getattr(cd[0][1], 'uncompressed',-1)),0)  for cd in zip(databases,range(len(databases)))  ])
  if res[0]!=0:
    sys.exit(-1)

  try:
    os.stat(os.path.join(PYCVF_DATABASE_DIR,".downloads"))
  except:
    os.mkdir(os.path.join(PYCVF_DATABASE_DIR,".downloads"))

  class ProgressBar:
    def __init__(self,d,text):
      self.d=d
      self.d.gauge_start(text)
    def update(self,percent):
      self.d.gauge_update(percent=percent)
    def __del__(self):
      self.d.gauge_end(text)

  import time

  for cd in res[1]:
    cd=int(cd)
    print cd
    print databases[cd][1]
    d.infobox("Installing database "+databases[cd][1]['title'])
    time.sleep(0.3)
    for url in databases[cd][1]['url']:
      pb=ProgressBar(d,"download of "+url)
      tempfilename= os.path.join(os.path.join(PYCVF_DATABASE_DIR,".downloads"),os.path.basename(url))
      download( url,tempfilename,pb.update)
      del pb
      d.infobox("Decompressing file "+tempfilename)
      for op in databases[cd][1]['decompress']:
        ntempfilename=op(tempfilename)
        os.unlink(tempfilename)
        tempfilename=ntempfilename
      if (databases[cd][1].haskey('post_install')):
        os.system(databases[cd][1]['postinstall'])


import setuptools
class install_databases(setuptools.Command):
    description = "install databases by downloading them from the web"
    user_options=[]

    def initialize_options (self):
        pass
    def finalize_options (self):
        pass 
    def run (self):
        main()

if __name__=="__main__":
  main()
