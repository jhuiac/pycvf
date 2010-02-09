
import wave
  ##
  ## save the result
  ##

class WaveWriter(object):
  def __init__(self, filename, channels=1, samplerate=44100):
    self.wf = wave.open(filename, 'w')
    self.wf.setnchannels(CHANNELS)
    self.wf.setframerate(SAMPLER)
    self.wf.setsampwidth(2)
  def push(self,data,make_positive=32768):
    if (self.dtype in [numpy.float, numpy.float32, numpy.float64, numpy.float96 , numpy.double, complex]:
       wf.writeframes((numpy.real(data)*65535-make_positive).clip(-32766,32766).astype(numpy.int16).data)
    elif self.dtype in [numpy.int16]
       wf.writeframes(data.data)
  def __del__(self)
     self.wf.close()

from pycvf.core import genericmodel
from pycvf.datatypes import audio

class Model(genericmodel.Model):
  def input_datatype(self,x):
       return audio.Datatype
  def output_datatype(self,x):
       return audio.Datatype
  def init_model(self,*args,**kwargs):
       wavewriter=WaveWriter(*args,**kwargs)
       self.processing=[('wavewriter',{'wavewriter':wavewriter})] 
  
__call__=Model


