# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database builder By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys
import scipy,pylab

from jfli.project_specific.mvp import mvpaccess

from pycvf.lib.video.lazydisplay import *
from pycvf.lib.video.lazydisplayqt import *
from pycvf.lib.video.simplevideoreader7 import *

from pycvf.lib.graphics.zopencv import *
from pycvf.lib.graphics.colortransforms import *
from pycvf.lib.graphics.imgfmtutils import *

from pycvf.indexes.bssdbindex import *
from pycvf.indexes.indexbuilders import *
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *

#import pysift

#########################################################################################################################################
# Get access to databases
#########################################################################################################################################


mvp=mvpaccess.MvpAccess(with_ontology=False);
db1idx=MultidimensionalDb("/home/tranx/vdb/db1","db1",21)


#########################################################################################################################################
# The feature that we observe
#########################################################################################################################################


def extractfeatures(i,pts,fno):
    f1=i.mean()
    hueimg=rgb2hsv(i)
    h,w,d=hueimg.shape
    f2a=scipy.histogram(hueimg[:h//2,:w//2,0],bins=4,range=(0,256),normed=True)[0]
    f1a=i[:h//2,:w//2,:].mean()
    f2b=scipy.histogram(hueimg[h//2:,:w//2,0],bins=4,range=(0,256),normed=True)[0]
    f1b=i[h//2:,:w//2,:].mean()
    f2c=scipy.histogram(hueimg[h//2:,w//2:,0],bins=4,range=(0,256),normed=True)[0]
    f1c=i[h//2:,w//2:,:].mean()
    f2d=scipy.histogram(hueimg[:h//2,w//2:,0],bins=4,range=(0,256),normed=True)[0]
    f1d=i[:h//2,w//2:,:].mean()
    featurevector=numpy.hstack([array([f1,f1a,f1b,f1c]),fd,f2a,f2b,f2c,f2d])
    return featurevector
#    db1idx.add(featurevector,(filename,tps))





#########################################################################################################################################
# The video reader that we use
#########################################################################################################################################

filename=mvp.find_video(channel="ntv",year=2009,month=2,day=random.randint(1,10),hour=random.randint(10,20))
videoreader=SimpleVideoReader7(filename)

#########################################################################################################################################
# The model of the graph for the experiment
#########################################################################################################################################


observed_features=[
                    ('src[2]|rgb2hsv|extractfeatures|indexerdb1.f((filename,src[1]))'  , {'indexerdb1':IndexBuilder(db1idx, None ,False)
                                                           },
                                                     {'title':'db1','color':(1,0,0)}
                     ),
                     ('src[2]|rgb2hsv|extractfeatures|indexerdb1.f((filename,src[1]))'  , {'indexerdb1':IndexBuilder(db1idx, None ,False)
                                                           },
                                                     {'title':'db1','color':(1,0,0)}
                      ),

                    ]


#########################################################################################################################################
# No need for recording
#########################################################################################################################################

track=NullTrack(observed_features)

#########################################################################################################################################
# Link with all the required
#########################################################################################################################################

observer=MultipleObserver(map(lambda x:x[0],observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],observed_features),{})
contextadd['extractfeatures']=extractfeatures
observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x),dir(observer.context))+contextadd.values()))
#videoreader.set_observer(observer.proceed)
videoreader.observer=extractfeatures

#########################################################################################################################################
# Run
#########################################################################################################################################


videoreader.run()

ld=LazyDisplay()

########################################################################################################################################
########################################################################################################################################
########################################################################################################################################


