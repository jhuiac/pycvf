# -*- coding: utf-8 -*-

#import pyffmpeg_audioqueue as audioqueue
import audioqueue
import scipy
import numpy
from pycvf.core.errors import pycvf_warning



class FFTComputer:
  def __init__(self,_len=128,sigptp=65536,sigmean=0):
      self.filterwindow=numpy.ones((_len,1))
      self.sigmean=sigmean
      self.sigptp=sigptp
  def sig2fft(self,sig):
      sig=sig.astype(float)
      #sig+=((self.sigptp/2)-self.sigmean)
      sig/=(self.sigptp/2)
      #sig*=self.filterwindow
      #print sig.min(),sig.max()
      fftx=numpy.fft.fft(sig,axis=0)
      return fftx#numpy.abs(fftx),numpy.angle(fftx)
  def ifft2sig(self,xifft):
      return numpy.fft.ifft(xifft,axis=0)#xifft[0]+1J*xifft[1])

class EventReceiver(object):
  def __init__(self,sample_rate=44100,
                    dest_frame_size=512,
                    dest_frame_overlap=128+64+32+16+8,
                    tps=30,
                    fftc=FFTComputer
              ):
       self.audiohq=audioqueue.AudioQueue(limitsz=4) 
       self.audioq=audioqueue.AudioQueue(limitsz=12,
                                         tps=tps,
                                         samplerate=sample_rate,
                                         destframesize=dest_frame_size,
                                         destframeoverlap=dest_frame_overlap,
                                         destframequeue=self.audiohq
                                        )
       self.fftc=fftc(dest_frame_size)
  def push(self,x):
    self.audioq.push(x)
    
  def get(self):
    x=self.audiohq.get_nowait()
    return self.fftc.sig2fft(x[0])
                                                      
    ## if some data are ready push to 

class AudioSpectrumComputer(object):
    def __init__(self,*args,**kwargs):
      self.er=EventReceiver(*args,**kwargs)
    def push(self,rdr):
      rdr.set_observer(self.er.audioq.putforce)
      rdr.vr.step()   
      try:
        while True:
          try:
            yield self.er.get() #audiohq.get_nowait()
          except audioqueue.Queue_Empty:
            rdr.step()
      except StopIteration:
        pass
      except KeyboardInterrupt:
        raise


      
from pycvf.core import genericmodel
from pycvf.datatypes import audio

class Model(genericmodel.Model):
  def input_datatype(self,x):
       #assert(audio.Datatype.check(x))
       return audio.Datatype
  def output_datatype(self,x):
       return audio.Spectrum.Datatype
  def init_model(self,*args,**kwargs):
       audiospectrumcomputer=AudioSpectrumComputer(*args,**kwargs)
       self.processing=[('audiospectrumcomputer',{'audiospectrumcomputer':audiospectrumcomputer.push})] 

__call__=Model

if __name__=="__main__":
    from pycvf.core.builders import pycvf_builder
    vdb=pycvf_builder("LF('pycvf.databases.sound_directory','/media/c/music/musique/')")
    r=iter(vdb).next()
    x=audiospectrum(r[0])
#    print "x",x
    for a in x:
      print a
