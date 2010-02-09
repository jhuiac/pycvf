# -*- coding: utf-8 -*-
import os
from pycvf.core import settings


DISPLAY_DRIVER=settings.DISPLAY_DRIVER
if ("DISPLAY" not in os.environ or not(len(os.environ["DISPLAY"]))) and DISPLAY_DRIVER in [ "qt" , "pyglet" ]:
    from pycvf.core.errors import pycvf_warning
    pycvf_warning("No DISPLAY variable changing default displayt to 'caca'")
    DISPLAY_DRIVER="caca"

if DISPLAY_DRIVER=="pyglet":
  from pycvf.lib.video.render.pyglet_lazy import LazyDisplay
elif DISPLAY_DRIVER=="aa":
  from pycvf.lib.video.render.aa_lazy import LazyDisplay
elif DISPLAY_DRIVER=="caca":
  from pycvf.lib.video.render.caca_lazy import LazyDisplay
elif DISPLAY_DRIVER=="qt":
  from pycvf.lib.video.render.qt_lazy import LazyDisplayQt as LazyDisplay
else:
  raise ValueError, "For the moment, PyCVF only support one of the following video display : pyglet, aa, caca, qt" 


    