from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import urllib
import urllib2
import cookielib
import os
import numpy
import pyffmpeg
from pycvf.lib.graphics.imgfmtutils import *
import hashlib




class ReutersViewdle(object):
    def __init__(self):
        self.COOKIEFILE = '/tmp/'+str(os.getuid())+'-cookies.lwp'
        self.urlopen = urllib2.urlopen
        self.cj = cookielib.LWPCookieJar()
        self.Request = urllib2.Request
        if self.cj != None:
            if os.path.isfile(self.COOKIEFILE):
                self.cj.load(self.COOKIEFILE)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
            urllib2.install_opener(opener)
        self.hostbaseurl="http://reuters.viewdle.com"
    def _query(self,qstring,datefrom=None,dateto=None):
        if datefrom==None:
          datefrom=(2007,1,1)
        if dateto==None:
          import datetime
          d=datetime.datetime.today()-datetime.timedelta(1,0,0)
          dateto=(d.year,d.month,d.day)
        qdict={'q':qstring,'t':'','c':'','ddf':datefrom[2],'dmf':datefrom[1]-1,'dyf':datefrom[0],
               'ddt':dateto[2],'dmt':dateto[1]-1,'dyt':dateto[0],'gridView':'','pids':''}
        res=self.urlopen(self.hostbaseurl+"/search",urllib.urlencode(qdict)).read()
        return BeautifulSoup(res)
    def _get_videos_and_xml(self,res,no):
        self.curvideofileurl=res[no][0][0]
        self.curfacedetectfileurl=self.hostbaseurl+"/get/index/"+res[no][1]
        indexdatar=self.urlopen(self.curfacedetectfileurl).read()
        indexdata=BeautifulStoneSoup(indexdatar)
        return indexdata
    def get_faces(self,res,no):
        print "getting XML file..."
        self.xx=self._get_videos_and_xml(res,no)
        tt=False
        for p in self.xx.findAll("persona"):
            tr=[ (int(r['t']),int(r['x']),int(r['y']),int(r['w']),int(r['h'])) for r in p.findAll('r')]
            if (len(tr)==0):
                continue
            tt=True
        if (not tt):
            print "no facetrack info... skipping file..."
            return
        tmpfilename="/tmp/viewdleaxs-"+str(os.getuid())+"-"+hashlib.md5(self.curvideofileurl).hexdigest()+".flv"
        try:
            f=file(tmpfilename,"rb")
            f.close()
            print "using stored video..."
        except:
            print "downloading video..."
            f=file(tmpfilename,"wb")
            f.write(self.urlopen(self.curvideofileurl).read())
            f.close()
        print "processing video..."
        v=pyffmpeg.FFMpegReader()
        v.open(tmpfilename)
        for p in self.xx.findAll("persona"):
            sta_t=int(p.e['start'])
            end_t=int(p.e['end'])
            tr=[ (int(r['t']),int(r['x']),int(r['y']),int(r['w']),int(r['h'])) for r in p.findAll('r')]
            if (len(tr)==0):
                print "no facetrack info : skipping apparition of "+p['name']
                continue
            #tr.sort(cmp=lambda x,y:x[0])
            tr=numpy.array(tr,dtype=numpy.int)
            maxx=tr.max(axis=0)
            #assert(len(maxx)==5)
            tmaxx=maxx.reshape((5,))
            print "maxx:"+str(maxx)
            ci=0
            ltr=tr.shape[0]
            print tr.shape
            print "ltr:"+str(ltr)
            filenameout="facetrack-"+p["name"]+"-"+hashlib.md5(self.curvideofileurl).hexdigest()+"-"+str(sta_t)+".seq"
            #fileout=file(filenameout,"wb")
            #self.videowriter=VideoWriter()
            for t in range(sta_t,end_t):
                  if (ci+1<ltr):
                      if(tr[ci+1,0]<=t):
                            ci=ci+1
                  bx,by,dx,dy=tr[ci,1],tr[ci,2],tr[ci,3],tr[ci,4]
                  #print bx,by,dx,dy
                  print "."
                  maxx=tmaxx.copy()
                  rx=maxx[3]-dx
                  ry=maxx[4]-dy
                  nbx=bx-rx//2
                  nby=by-ry//2
                  rescalef=.5
                  bx*=rescalef
                  by*=rescalef
                  nbx*=rescalef
                  nby*=rescalef
                  dx*=rescalef
                  dy*=rescalef
                  bx-=dx/2
                  #by-=dy/2
                  maxx*=rescalef
                  trk=v.get_tracks()[0]
                  trk.seek_to_frame(t*25)
                  self.curi=trk.get_current_frame()[2]
                  #ld1.push((self.curi,0))
                  ni=numpy.zeros((int(maxx[4]),int(maxx[3]),3),dtype=numpy.uint8)
                  tpt=self.curi[int(by):int(by)+int(dy),int(bx):int(bx)+int(dx)]
                  #print dx,dy
                  #print (numpy.shape(tpt))
                  ttby=ry//2
                  ttbx=rx//2
                  #print tbx,tby
                  #print (numpy.shape(ni[ttby:(ttby+int(dy)),ttbx:(ttbx+int(dx))]))
                  print tpt.shape, ni.shape
                  ni[ttby:(ttby+int(tpt.shape[0])),ttbx:(ttbx+int(tpt.shape[1]))]=tpt
                  #ld2.push((self.curi[int(by):int(by)+int(dy),int(bx):int(bx)+int(dx)],0))
                  #self.curimg=Image.fromstring("RGBA",(self.curi.shape[1],self.curi.shape[0] ),data=self.curi.tostring())
                  #self.cface=self.curimg.crop((int(nbx),int(nby),int(maxx[3]),int(maxx[4])))
                  yield ni
                  #print "|"+str(t)
                  #self.cface=Image.fromstring("RGBA",(ni.shape[1],ni.shape[0] ),data=ni.tostring())
                  #print "/"+str(t)
                  #self.cface.save(filenameout+str(t)+".jpg","JPEG")
                  #print "\\"+str(t)
                  #self.videowriter.write(cface)
#            del self.videowriter
        os.remove(tmpfilename)
    def query(self,qstring,*args,**kwargs):
        res=self._query(qstring,*args,**kwargs)
        return map(lambda x:(x[7].split(","),x[1]) ,filter(lambda x:x[0]==u'showFlashObject(' ,map(lambda x:x['onclick'].split("'"),filter(lambda x:x.has_key("onclick"),res.findAll('a')))))


#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

from pycvf.datatypes import image
from pycvf.core import database

Fames=["Barack Obama",
       "Angela Merkel",
       "Ban Ki-Moon",
       "George Bush",
       "Frank-Walter Steinmeier",
       "Jean-Claude Trichet",
       "Hugo Chavez",
       "Condoleezza Rice",
       "Gordon Brown",
       "Dmitry Medvedev",
       "Hillary Clinton",
       "Nicolas Sarkozy",
       ]


class DB(database.ContentsDatabase,image.Datatype):
  def __init__(self,who=Fames[0],maxframes=100):
     self.who=who
     self.maxframes=maxframes
     self.rv=ReutersViewdle()
     self.rvq=self.rv.query(who)
     print self.rvq
  def __iter__(self):
      for x in range(len(self.rvq)):
         c=0
         for y in self.rv.get_faces(self.rvq,x):
            yield (y,self.who, x,c)
            c+=1
  
__call__=DB          
ContentsDatabase=DB
