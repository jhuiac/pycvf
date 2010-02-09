# -*- coding: utf-8 -*-
from pycvf.core import settings
    
if settings.AUDIO_DRIVER=="pyglet":
  from pycvf.lib.audio.render.pyglet_lazy import LazyAudioSink
elif settings.AUDIO_DRIVER=="alsa":
  from pycvf.lib.audio.render.alsa_lazy import LazyAudioSink
elif settings.AUDIO_DRIVER=="oss":
  from pycvf.lib.audio.render.oss_lazy import LazyAudioSink
else:
  raise ValueError, "For the moment, PyCVF only support one of the following audio drivers : pyglet, alsa, oss"



