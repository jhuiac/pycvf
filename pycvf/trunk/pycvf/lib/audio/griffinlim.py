# -*- coding: utf-8 -*-
##
## GRIFFIN & LIM ALGORITHM
##
##  For phase reconstruction from a magnitude spectrogram
##
##

##  Implementation Copyright (c)  Bertrand NOUVEL CNRS 2009.
##  All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions
##  are met:
##  1. Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##  2. Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in the
##     documentation and/or other materials provided with the distribution.
##  3. Neither the name of the University nor the names of its contributors
##     may be used to endorse or promote products derived from this software
##     without specific prior written permission.
##
##  THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
##  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
##  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
##  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
##  OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
##  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
##  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
##  OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
##  SUCH DAMAGE.


import numpy,sys


###
###  Ok we just included the hamming window there, but other window function may be implemented as needed
### 

from pycvf.lib.audio.windowing import hamming

##
## THIS IS GRIFFIN & LIM FOR SMALL SAMPLES 
## 

class GriffinLim:
  df=128
  di=128/8
  expd=1.001
  mulf=800.
  ww=None
  make_positive=32768
  def __init__(self,sz=None,delta=None,iter=33,ww=None):
     if (sz==None):
       sz=self.df
     if (delta==None):
       delta=self.di
     self.iter=iter
     if (ww!=None):
        self.ww=ww 
     if (self.ww==None):
       windowing.hamming(sz)
     self.sz=sz
     self.S=delta
     self.xt=numpy.zeros(self.sz)
     self.wsf=[]
  def signal_estimate(self,YW):
     ## eq.4
     yw=[None]*YW.shape[0]
     for m in range(YW.shape[0]):
        yw[m]=numpy.fft.ifft(numpy.roll(YW[m],-self.ww.shape[0]//2))*self.ww
     ## reconstruction of the signal by overlap add
     x=numpy.zeros(((YW.shape[0]+(self.sz-self.S)/self.S)*(self.S)))
     #print (x.shape[0]-do)/self.S
     #print yw[m].shape,self.wsf.shape
     #for m in range(YW.shape[0]):
     #   print yw[m].shape,x[(m*self.S):((m*self.S)+self.sz)].shape,self.wsf[(m*self.S):((m*self.S)+self.sz)].shape
     #   x[(m*self.S):((m*self.S)+self.sz)]+=(yw[m]/self.wsf[(m*self.S):((m*self.S)+self.sz)])
     for m in range(YW.shape[0]):
        try:
          #print yw[m].shape,x[(m*self.S):((m*self.S)+self.sz)].shape,self.wsf[(m*self.S):((m*self.S)+self.sz)]
          x[(m*self.S):((m*self.S)+self.sz)]+=(yw[m]/self.wsf[(m*self.S):((m*self.S)+self.sz)])
        except:
          print "shape error", yw[m].shape,x[(m*self.S):((m*self.S)+self.sz)].shape,self.wsf[(m*self.S):((m*self.S)+self.sz)].shape
          pass
     if (self.make_positive):
        x=x-x.mean()+self.make_positive # constrained well centered signal
     return x
  def _backward(self,XT):
    return self.signal_estimate(XT)
  def backward(self,XT):
     #NXT=(numpy.exp(numpy.log(10)*numpy.abs(XT)/self.mulf)-self.expd)*numpy.exp(1j*numpy.angle(XT))
     NXT=XT
     return self._backward(NXT)
  def _forward(self,xt):
     XO=[]
     for m in range(0,(xt.shape[0]-(self.df-self.di))/self.S,1):
       XO.append(numpy.roll(numpy.fft.fft(xt[(m*self.S):((m*self.S)+self.sz)]*self.ww),self.sz//2))
     XO=numpy.vstack(XO)
     return XO
  def forward(self,xt):
     XT=self._forward(xt)
     #A=(self.mulf*numpy.log10(self.expd+numpy.abs(XT))).clip(0,65535)
     #NXT=A*numpy.exp(1j*numpy.angle(XT))
     NXT=XT
     return NXT
  def optimize_est(self,XO,YNA):
     return YNA * numpy.exp(1j* numpy.angle(XO))
  def prepare_mask(self,YNA):
     self.wsf=numpy.zeros(((YNA.shape[0]+((self.sz-self.S)/self.S)+10)*(self.S)))
     for m in range(YNA.shape[0]+((self.sz-self.S)/self.S)):  
        s1=self.wsf[(m*self.S):((m*self.S)+self.sz)].shape[0]
        self.wsf[(m*self.S):((m*self.S)+self.sz)]+=(self.ww*self.ww)[:s1]
  def optimize(self,YNA,iter=None, observ=None):
     if (not(iter)):
        iter=self.iter
     self.prepare_mask(YNA)
     ##
     ## do an initial estimate of the signal from a random signal
     ## 
     XO=YNA*numpy.exp(numpy.random.random(YNA.shape)*numpy.pi*2j)  
     xt=self.signal_estimate(XO)
     ##
     ## iterate deconstruction / contruction to smooth the reconstruction
     ## 
     for i in range(iter):
        XO=self.optimize_est(self.forward(xt),YNA)
        xt=self.backward(XO)
        if (observ):
          observ(xt,XO)
     return xt

if __name__=="__main__":
  import pyffmpeg
  import wave  
  df=128
  di=128//12
  do=df-di
  make_positive=32768

  ##
  ## Read the audio file
  ## 

  TS_AUDIO={ 'audio1':(1, -1, {'hardware_queue_len':1000,'dest_frame_size':df, 'dest_frame_overlap':0} )}  
  class Observer():
    def __init__(self):
     self.ctr=0
     self.acc=[]
    def observe(self,x):
     self.ctr+=1
     self.acc.append(x[0])
  
  observer=Observer()
  f=sys.argv[1]
  observer.acc=[]
  rdr=pyffmpeg.FFMpegReader()
  rdr.open(f,track_selector=TS_AUDIO)    
  track=rdr.get_tracks()
  track[0].set_observer(observer.observe)
  try:
    rdr.run()
  except IOError:
    pass


  ##
  ## Get the signal by concatenating all the samples
  ##
  ds=numpy.dstack(observer.acc)
  xn=((ds.mean(axis=1).T.copy('C').reshape(ds.shape[0]*ds.shape[2],1)[:(((44100*3)//2048)*2048)]+make_positive).squeeze())/65535.
  del ds
  del observer

  ##
  ## Initialize our algorithm
  ##
  ww=hamming(df)
  GriffinLim.df=df
  GriffinLim.di=di
  GriffinLim.make_positive=0.5
  gl=modelinstance=GriffinLim(ww=ww)



  ##
  ## Computer the spectrogram
  ##  
  XO=modelinstance.forward(xn)
  YNA=numpy.abs(XO)
  r=gl.optimize(YNA,iter=4,YN=XO)


  ##
  ## save the result
  ##
  CHANNELS=1
  SAMPLER=44100
  wf = wave.open("res/ngl-"+ f.split('/')[-1].split('.')[0] +".wav", 'w')
  wf.setnchannels(CHANNELS)
  wf.setframerate(SAMPLER)
  wf.setsampwidth(2)
  wf.writeframes((numpy.real(r)*65535-make_positive).clip(-32766,32766).astype(numpy.int16).data)
  
  


