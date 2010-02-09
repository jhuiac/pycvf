# -*- coding: utf-8 -*-
try:             
    import ossaudiodev as oss
except:                    
    import oss   

class LazyAudioSink:
  def __init__(self,rate=44100,channels=2,fps=30):
       try:
         self.ao=oss.open_audio()
       except:
         self.ao=oss.open('w')
       if (hasattr(self.ao,'stereo')):
         self.ao.stereo(1)
       self.ao.speed(rate)
       if (hasattr(self.ao,'format')):
         self.ao.format(oss.AFMT_S16_LE)
       else:
         self.ao.setfmt(oss.AFMT_S16_LE)
       self.ao.channels(channels)
  def push(self,x):
     self.ao.write(x[0][1].data)
  def f(self,x):
     self.ao.write(x[1].data)
     
