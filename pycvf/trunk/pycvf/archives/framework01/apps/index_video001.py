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


import os
from pycvf.lib.video.simplevideoreader5 import  *
from jfli.project_specific.videoindex.track import *
from jfli.project_specific.videoindex.videoprocessor import *
from jfli.project_specific.videoindex.index import *
from jfli.project_specific.mvp.mvpaccess import *

######################################################################
#### WE DEFINE WHAT WE WANT TO ANALYSIS IN SOME WORDS OUR MODEL ######
######################################################################

##################  ( nodepath, contextcomplement, reportinfos)


observed_features= [
                    ('raw|red|xmean'  , {}, {'title':'rmean','color':(1,0,0)}),
                    ('raw|green|xmean', {}, {'title':'gmean','color':(0,1,0)}),
                    ('raw|blue|xmean' , {}, {'title':'bmean','color':(0,0,1)}),
#                    ('raw|blue|scipy.histogram(5,range=(0,255))[0]y|ac.f|quantize(3)|idxr1.f',
#                         {'ac':AutoCalibrate(rate=1),
#                          'idxr1':Indexer(SmallWordsIndex("/tmp/indexblue001.idx"),lambda:(player.getFileName(),player.getCurrentFrameNo()))},
#                         {'name':'autocalibrated blue histogram', 'palette':(lambda x:(0,0,x))} ),
                    ('raw|rgb2hsv|hsvhue|0.001+scipy.histogram(16,range=(0,360))[0]|scipy.log',
                      {},
                      {'name':'hue loghistogram','palette-name':'hsv'}),
                    ('raw|blue|pywt.wavedec2("db2",5)|element(0)', {},{'title':'wavelet approximation0'}),# 2d approx
                    ('raw|blue|pywt.wavedec2("db2",5)|element(1)[0]',{},{'title':'wavelet hdetail 1'}), # 2d detail h
                    ('raw|blue|pywt.wavedec2("db2",5)|element(2)[0]',{},{'title':'wavelet hdetail 2'}), # 2d detail h
                    ('raw|blue|pywt.wavedec2("db2",5)|element(3)[0]',{},{'title':'wavelet hdetail 3'}), # 2d detail h
                    ('raw|blue|pywt.wavedec2("db2",5)|element(1)[0]|xmap((lambda x:math.log(abs(x.mean())+0.001)))',
                     {},{'title':'mean of wavelet hdetail 1'}), #1d
                    ('raw|blue|pywt.wavedec2("db2",5)|element(1)[0]|xmap((lambda x:math.log(abs(x.var())+0.001)))',
                     {},{'title':''}), #1d
                    ('raw|red|tl.f|xmean',{'tl':TimeDifferencier()},{'title':'number of pixels affected by time difference'}), #0d
                    ('raw',{},{}),
                    ('raw|red|sobel|xabsdiff(current_cimage[diffimgname])',{'diffimgname':"raw|red|tl.f"},{}), #2d (fullres)
                    ('raw|rgb2hsv|hsvluminance|0.001+scipy.histogram(16,range=(0,255))[0]|scipy.log',{},{}) #1d
                   ]

###############################################################
###############################################################
###############################################################

# we are testing we dont expect to append new info to an existing
# track
try:
    for e in os.listdir("/tmp"):
        if (e[0:10]=="test.track"):
            os.remove("/tmp/"+e)
except:
    pass

###############################################################
######READ VIDEO AND COMPUTE TRACK#############################
###############################################################

mvp=MvpAccess()
year=2008
month=10
day=15
video=mvp.get(year,month,day)
filename=video['videofile']


#filename="/home/tranx/taiyou.flv"


track=OnDiskMultiTrackLargeZ("/tmp/test.track",meta={'model':observed_features,'video':video})
observer=MultipleObserver(map(lambda x:x[0],observed_features),track=track)
contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],observed_features),{})
observer.context=dict(zip(observer.context.keys()+contextadd.keys(),observer.context.values()+contextadd.values()))
videoreader=SimpleVideoReader5(filename,observer.iterproceed,start=0,stop=100)
observer.context['videoreader']=videoreader
videoreader.run()
track.saveindex()
track.savemeta()
del track
del svr
del observer


####################################################################
####DO SOME NICE REPORTS SO WE CAN ANALYZE OUR FEATURES ############
####################################################################

from jfli.project_specific.videoindex.reportgenerator import *

track=OnDiskMultiTrackLargeZ("/tmp/test.track")
layout=makesimplelayoutfromtrack(track)
rg=ReportGenerator("/tmp/report.pdf",track,layout)
del rg
del track
