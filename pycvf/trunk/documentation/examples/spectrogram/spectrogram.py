# -*- coding: utf-8 -*-
from pycvf.lib.audio.playalsa import *
from pycvf.lib.ui.qt import *
qapp.processEvents()

from pycvf.lib.ui.qtgrapher import *
from pycvf.lib.video.lazydisplayqt import *
import sys
import numpy 
import scipy
import pylab

qtg=QtGrapherDialog(numpy.zeros(10,),minv=0.,maxv=0.5)
qtg.show()
qtd=LazyDisplayQt()
qapp.processEvents()

from pyffmpeg import *
frate=44100.
freq=12
df=512
do=512-(512/freq)
di=df-do
nx=df//di

to=256
narr=numpy.zeros((to,df//2,3),dtype=numpy.uint8)
tsig=numpy.zeros(df//2)
t2sig=numpy.zeros(df//2)
ssig=0
cstate=numpy.zeros((3,df//2),dtype=numpy.uint8)

la=AlsaSoundLazyPlayer()
TS_AUDIO={ 'audio1':(1, -1, {'hardware_queue_len':1000,'dest_frame_size':df, 'dest_frame_overlap':do} )}
rdr=FFMpegReader()
rdr.open(sys.argv[1],track_selector=TS_AUDIO)

#pylab.ion()

class Observer():
  def __init__(self):
     self.ctr=0
  def observe(self,x):
     global narr, cstate, tsig, t2sig,ssig
     if (self.ctr%freq==0):
         la.push((x[0],x[1],x[2]))
     self.ctr+=1
     fftsig=numpy.fft.fft(x[0].mean(axis=1))
     spect=numpy.log2(1+numpy.abs(numpy.roll(fftsig,fftsig.shape[0]//2,axis=0)))[df//2:]
#   print spect.ptp()
     spect=spect/(32.+numpy.log2(fftsig.shape[0]))
     tsig+=spect
     t2sig+=spect**2
     ssig+=1
     spect-=(tsig/ssig)
     spect/=(0.000001+((abs((t2sig/ssig)-((tsig/ssig)**2)))**.5))
     #print spect
     #spect-=spect.mean()
     spect*=255
     spect=spect.clip(0,255)
     #spect+=127
     spect=spect.astype(numpy.uint8)
     #print "f2,f1,f0", frate/(df/(1+scipy.argsort(spect)[-3:]))
     if (self.ctr%30==0):
       r=numpy.log2(1+numpy.arange(spect.shape[0]))
       pylab.clf()
       pylab.xlim(-512,512)
       pylab.ylim(-512,512)       
       pylab.plot(numpy.real(numpy.exp(2J*(r%1.)*numpy.pi)*spect) ,
                 numpy.imag(numpy.exp(2J*(r%1.)*numpy.pi)*spect),  )
       pylab.savefig("spect-%d.png"%(self.ctr))
     #pylab.show()
     #print spect.min()
     #print spect.max()
     pstate=cstate[1,:]*.9
     #print pstate.shape, spect.shape
     pstatesel=(pstate>spect)
     cstate[0,pstatesel]=pstate[pstatesel]
     #print pstatesel, -pstatesel
     cstate[0,-pstatesel]=spect[-pstatesel]
     #+max(cstate[0]*.3,spect)
     narr[0,:,0]=255-cstate[1,:]
     narr[0,:,1]=255-cstate[1,:]
     narr[0,:,2]=255
     qtd.f(narr)
     narr=numpy.roll(narr,1,axis=0)
     cstate=numpy.roll(cstate,1,axis=0)     
     #qtg.f(spect/(32.+numpy.log2(fftsig.shape[0])))#/(65536.*fftsig.shape[0]))
     qapp.processEvents()
     
observer=Observer()

print "setting up"
track=rdr.get_tracks()
track[0].set_observer(observer.observe)
try:
  rdr.step()
except:
  pass

print "run"
rdr.run()
qapp.hide()
