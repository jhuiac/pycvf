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


import sys
import numpy as np
import scipy
import time
import ctypes
import re
import os
from jfli.signal.blockops_opts import *
from pycvf.lib.graphics.wavelets.filters import *
from pywt import *
from pycvf.lib.graphics.imgfmtutils import *
from opencv import cv
# import kdtrees
import ann

from jfli.project_specific.mvp.mvpaccess import *

from pycvf.lib.video.simplevideoreader import *
from pycvf.lib.video.simplevideoreader2 import *
from pycvf.lib.video.simplevideoreader3 import *
from pycvf.lib.video.simplevideoreader4 import *

from pycvf.lib.video.sinks.numpysinks import *
from pycvf.lib.video.filters.numpyfilter import *

from pycvf.lib.misc.calendar import *
from jfli.project_specfic.mvp.mvpaccess import *

gobject.threads_init()


#registry = gst.registry_get_default ()

def thefunc(img):
    print "mean:" + str(mean(img))

class obj:
    def __init__(self):
        self.x=[]
    def f(self,img):
        m=mean(img)
        print "mean:" + str(m)
        self.x.append(m)

o=obj()
observer=TSSinkRGB(o.f)
xobserver=FiltNumpyRGB(o.f)


mvp=MvpAccess()


#observer=Observer()
#for year in range(2001,2009):
#    for month in range(0+1,12+1):
#        for days in range(0+1,lenmonth(year,month)+1):

year=2008
month=10
day=15
if True:
            try:
                video=mvp.get(year,month,day)
                svr=SimpleVideoReader5(video['videofile'],xobserver)
                print "running"# >> sys.stderr
                svr.run()
#                process_movie(filename,filter)
            except:
                print ("unable to process video for %04d-%02d-%02d"%(year,month,day))

print o.x



### sample random images in the database :
### for instance we want to compute mean Fourier coefficients and stddev coefficients


## this first implementation involves to memorize 10000 fftscan .... not very efficient
## better use an Aucocalibrate object...
for i in range(10000):
    year=random.choice(range(2001,2008))
    month=random.choice(range(0+1,12+1))
    days=random.choice(range(0+1,lenmonth(year,month)+1))
    img=random.choice(range(3600))
    svr=SimpleVideoReader5(video['videofile'],xobserver,start=img,stop=img+1)
    svr.run()
xo=numpy.dstack(o.memproceed)
del o
meanfft=xo.mean(axis=2)
varfft=xo.var(axis=2)



###
###

import os
from pycvf.lib.video.simplevideoreader5 import  *
from jfli.project_specific.videoindex.imagesignature import *
from jfli.project_specific.videoindex.track import *
from jfli.project_specific.videoindex.report_generator import *

os.remove("/tmp/test.track")

observed_features= ['raw|red|xmean', # 0d
                    'raw|green|xmean', # 0d
                    'raw|blue|xmean', # 0d
                    'raw|blue|scipy.histogram(5,range=(0,255))|numpy.array.[ac]f', #0d
                    'raw|rgb2hsv|hsvhue|scipy.histogram(16,range=(0,360))', # 1d
                    'raw|blue|pywt.wavedec2("db2",5)|element(0)', # 2d
                    'raw|blue|pywt.wavedec2("db2",5)|element(1)|xmap(xmean)', #1d
                    'raw|blue|pywt.wavedec2("db2",5)|element(1)|xmap(xvar)', #1d
                    'raw|red|tl.f|xmean', #1d
                    'raw|red|sobel|xabsdiff(current_cimage[diffimgname])', #2d (fullres)
                    'raw|rgb2hsv|hsvluminance|scipy.histogram(16,range=(0,255))' #
                   ]


track=OnDiskTrack("/tmp/test.track")
o=MultipleObserverOnDiskTrack(observed_features,track=track)
o.context['tl']=TimeDifferencier()
o.context['ac']=AutoCalibrate(rate=1)
o.context['diffimgname']="raw|red|tl.f"
fn="/home/tranx/=ripslyme.taiyoutobikini.flv"
svr=SimpleVideoReader5(fn,o.iterproceed,start=0,stop=100)
svr.run()
del track
del svr
del o

track=OnDiskTrack("/tmp/test.track")
layout=makesimplelayoutfromtrack(track,elements)
rg=ReportGenerator("/tmp/report.pdf",track,layout)
del rg
del track
