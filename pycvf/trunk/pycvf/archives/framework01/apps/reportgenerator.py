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


# -*- coding: utf-8 -*-
import pylab ## get pylab for palette...
import numpy 
from reportlab.lib.units import cm
from reportlab.pdfgen.pycanvas import Canvas
from reportlab.lib.pagesizes import *
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.graphics.rescale import *
import math
import random

class Report0d:
    """ This class is used to represent part of the track that remember at each frame some 0d information
        such as a numerical value
    """
    def __init__(self,trackextractorf,trackno,meta,color=None,style=None,min=None,max=None):
        if color==None:
            color=(random.random(),0,random.random())
        self.extractorf=trackextractorf
        self.trackno=trackno
        self.meta=meta
        self.name=("title" in meta.keys()) and meta["title"] or None
        self.color=color
        self.style=style
        self.min=min
        self.max=max

class Report1d:
    """ This class is used to represent part of the track that remember at each frame some 1d information
        such as spectruns
    """
    def __init__(self,trackextractorf,trackno,meta,min=None,max=None):
        self.extractorf=trackextractorf
        self.trackno=trackno
        self.meta=meta
        self.name=("title" in meta.keys()) and meta["title"] or None
        self.min=min
        self.max=max
        
class Report2d:
    """ This class is used to represent part of the track that remember at each frame some essentially 2d information
        such as images
    """
    def __init__(self,trackextractorf,trackno,meta):
        self.extractorf=trackextractorf
        self.trackno=trackno
        self.meta=meta
        self.name=("title" in meta.keys()) and meta["title"] or None


from reportlab.lib.pagesizes import A4
(A4w,A4h)=A4
A4L=(A4h,A4w)

def fcompose(f1,f2):
    def rf(*args,**kwargs):
        return f1(f2(*args,**kwargs))
    return rf

def makesimplelayoutfromtrack(track,elements, onlywihtitle=True):
    """ This function creates a default layout from the track and it metadata """
    class TrackExtractor:
        def __init__(self,trackno):
            self.trackno=trackno
        def extract(self,frame):
            return frame[self.trackno]
    section0d_e=[]
    section1d_e=[]
    section2d_e=[]
    
    for sti in range(len(track[0])):
        st=track[0][sti]
        if ("title" in elements[sti].keys()):
          if (isinstance(st,numpy.ndarray)):
            if (numpy.asarray(st).squeeze().ndim==0):
                section0d_e.append(Report0d( fcompose(lambda x:numpy.asarray(x).squeeze(),  TrackExtractor(sti).extract),sti,elements[sti]))            
            elif (numpy.asarray(st).squeeze().ndim==1):
                section1d_e.append(Report1d( fcompose(lambda x:numpy.asarray(x).squeeze(), TrackExtractor(sti).extract),sti,elements[sti]))
            else:
                if (numpy.asarray(st).squeeze().ndim==2):
                    section2d_e.append(Report2d( fcompose( lambda x:numpy.asarray(x).squeeze(), TrackExtractor(sti).extract),sti,elements[sti]))
                elif ((numpy.asarray(st).squeeze().ndim==3)  and (st.shape[2]==3)):
                    section2d_e.append(Report2d(  fcompose( lambda x:numpy.asarray(x).squeeze(), TrackExtractor(sti).extract),sti,elements[sti]))
                else:
                    print "warning don't know how to handle tracks in dimension higher than 2"
          elif (isinstance(st,list) or (type(st)==list) or (type(st)==tuple)):
            if ((type(st[0])==int) or  (type(st[0])==float)or  (type(st[0])==numpy.float64)):
              section1d_e.append(Report1d(TrackExtractor(sti).extract,sti,elements[sti]))
            else:
              print "warning list of unhandled data : unknow datatype:"+str(type(st))
          elif ((type(st)==int) or  (type(st)==float)or  (type(st)==numpy.float64)):  
            section0d_e.append(Report0d(TrackExtractor(sti).extract,sti,elements[sti]))
          else:
            print "warning unhandled data : unknow datatype:" + str(type(st))
    return {
            'pagesize':A4L,
            'imagesinwidth':8,
            'sections':(len(section0d_e) and
                        [{'name':'graphs',
                         'mode':0,
                         'layoutweight':1+len(section0d_e),
                         'elements':section0d_e                           
                        }] or [])
                        +(len(section1d_e) and
                        [{'name':'spectrograms',
                         'mode':1,
                         'layoutweight':1+len(section1d_e),
                         'elements':section1d_e                           
                        }] or [])
                        +(len(section2d_e) and
                        [{'name':'images',
                         'mode':2,
                         'layoutweight':1+len(section2d_e),
                         'elements':section2d_e                           
                        }] or [] )
            }


class ReportGenerator(object):
    def report_draw_section(self,canvas,track,btime,etime,box,section,layout): 
            ### draw each section
            s=section
            mode=s['mode']
            bx,by,dx,dy=box
            if (mode==0):
                nbx=bx+0.5*cm
                ndx=dx-0.5*cm
                for e in s['elements'] :
                    datas=numpy.array([ e.extractorf(track[i]) for i in range(btime,etime)  ])
                    if e.min:
                        minv=e.min
                    else:
                        minv=datas.min()
                    if e.max:
                        maxv=e.max
                    else:
                        maxv=datas.max()
                    if (maxv==None):
                      break
                    eq=maxv-minv                        
                    if (eq==0):
                         eq=1
                    ### transform datas in a displayble form
                    canvas.setStrokeColorRGB(*e.color)
                    datas=by+(((datas-minv)/eq)*dy)
                    step=float(dx)/len(datas)
                    points=zip(nbx+numpy.array(range(0,ndx+step,step)),datas)
                    lines=map(lambda x,y:(x[0],x[1],y[0],y[1]),points[:-1],points[1:])
                    canvas.lines(lines)
                    canvas.drawString(lines[0][0]-(0.5*cm), lines[0][1], "T"+ str(e.trackno))
            if (mode==1):
                ne=(len(s['elements']))
                for e in range(ne) :
                    re=s['elements'][e]
                    nbox=(bx+0.5*cm,by+dy-(e+1)*(float(dy)/ne),dx-0.5*cm,(float(dy)/ne))
                    nbx,nby,ndx,ndy=nbox
                    datas=[ re.extractorf(track[i]) for i in range(btime,etime)  ]
                    datas=numpy.array(datas,dtype=numpy.float)
                    minv=datas.min()
                    maxv=datas.max()
                    eq=maxv-minv
                    if (eq==0):
                         eq=1
                    datas=(((datas-minv)*255.)/eq)
                    cmx=[pylab.cm.jet,pylab.cm.hot,pylab.cm.hsv][e%3]
                    res=(lambda y: [x for x in cmx(y)])(datas)
                    ar=numpy.array(res).swapaxes(0,1)*255
                    #print "1del"+str(numpy.shape(ar))
                    #print "1del"+str(numpy.shape(ar[:,:,:3]))
                    vres=NumPy2PIL(ar[:,:,:3].astype(numpy.uint8))
                    points=[(nbx-(0.5*cm),nby),(nbx+ndx,nby),(nbx+ndx,nby+ndy),(nbx-(0.5*cm),nby+ndy),(nbx-(0.5*cm),nby)]
                    lines=map(lambda x,y:(x[0],x[1],y[0],y[1]),points[:-1],points[1:])
                    canvas.lines(lines)
                    canvas.drawString(lines[0][0], lines[0][1], "T"+ str(re.trackno))
                    #print lines
                    canvas.drawInlineImage(vres,x=nbx,y=nby,width=ndx,height=ndy) # for images that don't repeat
            if (mode==2):
                ne=(len(s['elements']))
                for e in range(ne) :
                    re=s['elements'][e]
                    nbox=(bx+0.5*cm,by+dy-(e+1)*(float(dy)/ne),dx-0.5*cm,(float(dy)/ne))
                    nbx,nby,ndx,ndy=nbox
                    ew=layout['imagesinwidth']
                    ew=ndx//8
                    datas= re.extractorf(track[btime])
                    sh=datas.shape
                    odx=sh[0]
                    ody=sh[1]
                    #ew=(ndy*odx/ody)
                    enw=max(1,ndx//(ew))
                    for ni in range(enw):
                        nndx=ndx/enw 
                        nnbx=nbx+ni*nndx
                        t=int(btime+( (etime-btime)* (ni/enw)))
                        datas= re.extractorf(track[t])
                        if (datas.dtype!=numpy.uint8): 
                            maxv=datas.max()
                            minv=datas.min()
                            eq=maxv-minv
                            datas.astype(numpy.float)
                            datas=(((datas-minv)/eq)*255)
                        vres=NumPy2PIL(datas.astype(numpy.uint8))
                        # preserve aspect ratio
                        sh=datas.shape
                        odx=sh[1]
                        ody=sh[0]
                        if (nndx/odx)>(ndy/ody):
                            nndx=(ndy*odx/ody)  
                        else:
                            ndy=(nndx*ody/odx)
                        points=[(nnbx-(0.5*cm),nby),(nnbx+nndx,nby),(nnbx+nndx,nby+ndy),(nnbx-(0.5*cm),nby+ndy),(nnbx-(0.5*cm),nby)]
                        lines=map(lambda x,y:(x[0],x[1],y[0],y[1]),points[:-1],points[1:])
                        canvas.lines(lines)
                        #canvas.drawString(lines[0][0], lines[0][1], "T"+ str(re.trackno))
                        canvas.drawInlineImage(vres,x=nnbx,y=nby,width=nndx,height=ndy) # for images that don't repeat
                        
            
    def draw_rule(self,canvas,p):    
          L=self.L
          l=self.l            
          tickers=[p*self.speed,min((p+1)*self.speed,self.lt)]
          canvas.setFont("Helvetica", 8)
          xtick=math.pow(10,math.floor(math.log(self.speed,10)-0.3))
          ztick=max(1,math.pow(10,math.floor(math.log(self.speed,10)-2.3)))
          btick=tickers[0]
          ltick=tickers[1]-tickers[0]
          leftrule=1*cm+0.5*cm+0.5*cm
          lenrule=self.hspace-(0.5*cm+0.5*cm)
          canvas.line(leftrule+float(tickers[0]-btick)/ltick*lenrule,3*cm,leftrule+float(tickers[0]-btick)/ltick*lenrule,2.5*cm)
          canvas.line(leftrule+float(tickers[1]-btick)/ltick*lenrule,3*cm,leftrule+float(tickers[1]-btick)/ltick*lenrule,2.5*cm)
          canvas.drawString(leftrule+float(tickers[0]-btick)/ltick*lenrule,2.1*cm, str(tickers[0]))
          canvas.drawRightString(leftrule+float(tickers[1]-btick)/ltick*lenrule,2.1*cm, str(tickers[1]))
          begtick=((tickers[0]//ztick)+1)
          endtick=((tickers[1]//ztick))
          for tick in range(begtick,endtick,ztick):
            dh=(math.log(tick,10)-math.log(ztick,10))
            if (dh%1.<0.00001):
                dh=0.1+(0.2*dh/2.)*cm
            else:
                dh=0.1*cm;
            canvas.line(leftrule+float(tick-btick)/ltick*lenrule,3*cm,leftrule+float(tick-btick)/ltick*lenrule,3*cm-dh)
          begtick=((tickers[0]//xtick)+1)
          endtick=((tickers[1]//xtick))
          for xtick in range(begtick,endtick,xtick):
            canvas.drawString(leftrule+float(xtick-btick)/ltick*lenrule,2.1*cm, str(xtick))
            
        
    def draw_template(self,canvas,p):
            ### draw page main layout
          L=self.L
          l=self.l                        
          canvas.setLineWidth(1)
          canvas.setStrokeColorRGB(0,0,0)
          canvas.setFillColorRGB(0,0,0)
          canvas.setFont("Helvetica", 10)
          canvas.line(1*cm,1*cm,L-1*cm,1*cm)
          canvas.line(1*cm,l-1*cm,L-1*cm,l-1*cm)
          canvas.drawString(1 * cm, 1.1 * cm, "analysis of video")
          canvas.drawRightString(L-1 * cm, 1.1 * cm, ("page %d of %d" % (p+1,self.numpages)))
          canvas.line(1*cm,2*cm,L-1*cm,2*cm)

          
    def put_plot1d(self,canvas,datas,nbox):
            pylab.clf()
            pylab.plot(datas)            
            pylab.savefig("/tmp/.rg.png")
            img=Image.open("/tmp/.rg.png")
            self.put_img(canvas, PIL2NumPy(img).astype('uint8').mean(axis=2).copy('C'), nbox)
          
    def put_img(self,canvas,datas,nbox,maxv=None,minv=None):
            nbx,nby,ndx,ndy=nbox
            if (datas.dtype!=numpy.uint8):
                 if (maxv==None): 
                   maxv=datas.max()
                 if (minv==None):
                   minv=datas.min()
                 eq=maxv-minv
                 datas.astype(numpy.float)
                 datas=(((datas-minv)/eq)*255)
            vres=NumPy2PIL(datas.astype(numpy.uint8))
            # preserve aspect ratio
            sh=datas.shape
            odx=sh[1]
            ody=sh[0]
            if (ndx/odx)>(ndy/ody):
                ndx=(ndy*odx/ody)  
            else:
                ndy=(ndx*ody/odx)
            #canvas.drawString(lines[0][0], lines[0][1], "T"+ str(re.trackno))
            canvas.drawInlineImage(vres,x=nbx,y=nby,width=ndx,height=ndy) # for images that don't repeat
 

                        
    def subtrack_analysis(self,canvas, track,subtrack):
        from jfli.dimred import PCA
        from pycvf.lib.stats.models import SimpleMeanVarianceModel, DimReducedModel
        lent=len(track.index)
        #m=ShapePreserving(SimpleMeanVarianceModel())
        m=SimpleMeanVarianceModel()
        ####
        maxt=[]
        mint=[]
        meant=[]
        stdt=[]
        m2=None
        e0=track[0][subtrack]
        if (e0==None):
            return
        nd=e0.squeeze().ndim
        if (nd==0):
              print "specific display for e[0] not yet... but soon (bigrams/graph| histograms|gmm|entropy...)"
        if (nd==1):
            if (e0.shape[0]>3):
              if (e0.shape[0]<1100):
                pcashp=e0.shape
                m2fpattern=lambda x:numpy.array([i])
                m2=DimReducedModel(PCA.IncrementalPCAdimred(e0.shape[0],20),SimpleMeanVarianceModel(),burnin=10)
                ipca=m2.dimreduc                
              else:
                   print "dimension too large not yet supported"
        if (nd==2) or (nd==3):
            flatshp=reduce(lambda x,y:x*y,e0.shape,1)
            pcashp=e0.shape
            m2fpattern=lambda x:numpy.array([i.reshape(flatshp)])
            if (flatshp>1100):
                print "running PCA over 1100 is a bit cumbersome... making things simplers"
                if ((nd==2) or (e0.shape[2]==1)):
                   m2fpattern=lambda x:(Rescaler2d((24,32)).process(x)).reshape(1,32*24)
                   pcashp=(24,32)
                   m2=DimReducedModel(PCA.IncrementalPCAdimred(32*24,20),SimpleMeanVarianceModel(),burnin=10)
                   ipca=m2.dimreduc
                else: 
                  print "hmm, actually it is a yet unsupported mode..."
                  m2=None
            else:
              m2=DimReducedModel(PCA.IncrementalPCAdimred(flatshp,20),SimpleMeanVarianceModel(),burnin=10)
              ipca=m2.dimreduc
        for x in range(lent):
            i=track[x][subtrack]
            maxt.append(i.max())
            mint.append(i.min()) 
            meant.append(i.mean())
            stdt.append(i.std())
            m.train([i],online=True)
            if (m2):
#                print "\r",x
                m2.train(m2fpattern(i),online=True)
                
        if (m2):
            m2.dimreduc.recompute()
        maxv=max(maxt)
        minv=min(mint)
       
        self.draw_template(canvas,-100)   
        (bx,by,dx,dy)=(2*cm,2*cm,self.L-4*cm,self.l-4*cm)
        ### draw each section            
        canvas.setFont("Helvetica", 11)
        canvas.drawString(bx+1.1*cm, by + dy - 1.1 * cm, "%dd-Subtrack %d"%(nd,subtrack,))
        canvas.setFont("Helvetica", 8)
        canvas.drawString(bx+4.1*cm, by + dy - 1.7 * cm, track.meta[subtrack]["title"])
        canvas.setFont("Helvetica", 8)
        canvas.drawString(bx+1.3*cm, by + dy - 2.3 * cm, "Mean Value / Std Value : %f / %f | Range (%f-%f)"%(numpy.mean(meant),numpy.mean(stdt),minv,maxv))

        if (nd==0):
            self.put_plot1d(canvas, numpy.histogram(numpy.array(meant),bins=256)[0], (bx+0.5*cm,by+(6*cm),5*cm,5*cm))
        if (nd==1):
            self.put_plot1d(canvas, m.mean(), (bx+0.5*cm,by+(6*cm),5*cm,5*cm))
            self.put_plot1d(canvas, m.std(), (bx+6*cm,by+(6*cm),5*cm,5*cm))            
            if (m2):
              canvas.drawString(bx+0.5*cm,by+(2.7*cm), "PCA")
              self.put_plot1d(canvas, m2.dimreduc.M[0,:], (bx+0.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
              self.put_plot1d(canvas, m2.dimreduc.M[1,:], (bx+3.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
              self.put_plot1d(canvas, m2.dimreduc.M[2,:], (bx+6.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
              self.put_plot1d(canvas, m2.dimreduc.M[3,:], (bx+9.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
              self.put_plot1d(canvas, m2.dimreduc.M[4,:], (bx+12.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))            
              self.put_plot1d(canvas, m2.dimreduc.M[5,:], (bx+15.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))                                    
        if (nd==2):
            self.put_img(canvas, m.mean(), (bx+0.5*cm,by+(6*cm),5*cm,5*cm), maxv=maxv, minv=minv)
            self.put_img(canvas, m.std(), (bx+6*cm,by+(6*cm),5*cm,5*cm))
            canvas.drawString(bx+0.5*cm,by+(2.7*cm), "PCA")
            self.put_img(canvas, m2.dimreduc.M[0,:].reshape(pcashp), (bx+0.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
            self.put_img(canvas, m2.dimreduc.M[1,:].reshape(pcashp), (bx+3.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
            self.put_img(canvas, m2.dimreduc.M[2,:].reshape(pcashp), (bx+6.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
            self.put_img(canvas, m2.dimreduc.M[3,:].reshape(pcashp), (bx+9.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))
            self.put_img(canvas, m2.dimreduc.M[4,:].reshape(pcashp), (bx+12.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))            
            self.put_img(canvas, m2.dimreduc.M[5,:].reshape(pcashp), (bx+15.5*cm,by+(2.7*cm),2.5*cm,2.5*cm))                        
          #  self.put_img(canvas, m2.dimreduc.IM[0,:].reshape(pcashp), (bx+9.5*cm,by+(2*cm),2.5*cm,2.5*cm), maxv=maxv, minv=0)                        
          #  self.put_img(canvas, m2.dimreduc.IM[1,:].reshape(pcashp), (bx+12.5*cm,by+(2*cm),2.5*cm,2.5*cm), maxv=maxv, minv=0)                                    
          #  self.put_img(canvas, m2.dimreduc.IM[2,:].reshape(pcashp), (bx+15.5*cm,by+(2*cm),2.5*cm,2.5*cm), maxv=maxv, minv=0)                                                
          #  self.put_img(canvas, m2.dimreduc.M[:,0].reshape(pcashp), (bx+0.5*cm,by+(0*cm),2.5*cm,2.5*cm), maxv=maxv, minv=minv)
          #  self.put_img(canvas, m2.dimreduc.M[:,1].reshape(pcashp), (bx+3.5*cm,by+(0*cm),2.5*cm,2.5*cm), maxv=maxv, minv=0)
          #  self.put_img(canvas, m2.dimreduc.M[:,2].reshape(pcashp), (bx+6.5*cm,by+(0*cm),2.5*cm,2.5*cm), maxv=maxv, minv=0)            
          #  self.put_img(canvas, m2.dimreduc.IM[:,0].reshape(pcashp), (bx+0.5*cm,by+(0*cm),2.5*cm,2.5*cm))
          #  self.put_img(canvas, m2.dimreduc.IM[:,1].reshape(pcashp), (bx+3.5*cm,by+(0*cm),2.5*cm,2.5*cm))                                    
          #  self.put_img(canvas, m2.dimreduc.IM[:,2].reshape(pcashp), (bx+6.5*cm,by+(0*cm),2.5*cm,2.5*cm))                                                            
          #  self.put_img(canvas, m2.dimreduc.IM[:,3].reshape(pcashp), (bx+6.5*cm,by+(0*cm),2.5*cm,2.5*cm))                                                                        
        canvas.showPage()
        canvas.save()

        
        
    def report_draw_section_legend(self,canvas,track,btime,etime,box,section,layout): 
            ### draw each section
            s=section
            mode=s['mode']
            bx,by,dx,dy=box
            if (mode==0):
                nbx=bx+0.5*cm
                ndx=dx-0.5*cm
                ne=(len(s['elements']))
                for e in range(ne) :
                    re=s['elements'][e]                    
                    canvas.setStrokeColorRGB(*re.color)
                    nbox=(bx+0.5*cm,by+dy-(e+1)*(float(dy)/ne),dx-0.5*cm,(float(dy)/ne))
                    nbx,nby,ndx,ndy=nbox
                    points=[(nbx-10,nby),(nbx+ndx+10,nby),(nbx+ndx+10,nby+ndy),(nbx-10,nby+ndy),(nbx-10,nby)]
                    lines=map(lambda x,y:(x[0],x[1],y[0],y[1]),points[:-1],points[1:])
                    canvas.lines(lines)
                    canvas.drawString(lines[0][0], lines[0][1], "T"+str(re.trackno) + ":" + str(re.meta))
            if (mode==1):
                ne=(len(s['elements']))
                for e in range(ne) :
                    re=s['elements'][e]
                    nbox=(bx+0.5*cm,by+dy-(e+1)*(float(dy)/ne),dx-0.5*cm,(float(dy)/ne))
                    nbx,nby,ndx,ndy=nbox
                    points=[(nbx-10,nby),(nbx+ndx+10,nby),(nbx+ndx+10,nby+ndy),(nbx-10,nby+ndy),(nbx-10,nby)]
                    lines=map(lambda x,y:(x[0],x[1],y[0],y[1]),points[:-1],points[1:])
                    canvas.lines(lines)
                    canvas.drawString(lines[0][0], lines[0][1], "T"+str(re.trackno) + ":" + str(re.meta))                    
            if (mode==2):
                ne=(len(s['elements']))
                for e in range(ne) :
                    re=s['elements'][e]
                    nbox=(bx+0.5*cm,by+dy-(e+1)*(float(dy)/ne),dx-0.5*cm,(float(dy)/ne))
                    nbx,nby,ndx,ndy=nbox
                    points=[(nbx-10,nby),(nbx+ndx+10,nby),(nbx+ndx+10,nby+ndy),(nbx-10,nby+ndy),(nbx-10,nby)]
                    lines=map(lambda x,y:(x[0],x[1],y[0],y[1]),points[:-1],points[1:])
                    canvas.lines(lines)                    
                    canvas.drawString(lines[0][0], lines[0][1], "T"+str(re.trackno) + ":" + str(re.meta))                    
                        
    def do_page(self,p,canvas):
            draw_meth=self.report_draw_section
            if (p==-1):
              draw_meth=self.report_draw_section_legend
            L=self.L
            l=self.l
            track=self.track
            ### draw page main layout
            self.draw_template(canvas, p)
            if (p!=-1):
              self.draw_rule(canvas,p)
            ### 
            for s in self.report_layout['sections']:
                ### draw section box
                (bx,by,dx,dy)=s['outerbox']
                canvas.setStrokeColorRGB(1,0,0)
                canvas.line(bx,by+dy,bx+dx,by+dy)
                canvas.setStrokeColorRGB(0,0,0)
                canvas.setFillColorRGB(0,0,0)
                canvas.drawString(bx,by+dy-0.4*cm,"section : "+s["name"])
                canvas.setStrokeColorRGB(0,0,1)
                canvas.line(bx,by+dy-0.5*cm,bx+dx,by+dy-0.5*cm)
                ### draw the section it self
                draw_meth(canvas,track,p*self.speed,min((p+1)*self.speed,self.lt),s['innerbox'],s,self.report_layout)
            ### draw each section            
            canvas.showPage()
            canvas.save()

    def __init__(self,filename,track,report_layout=None, speed=250):
        """for now the constructor directly create a report on the disk
            if no layout is specified this one is automatically constructed from the track.
            
            the speed parameters defines the scale at which you want to observe the datas
         """
        if (not report_layout):
           report_layout=makesimplelayoutfromtrack(track,track.meta)
        canvas=Canvas(filename,pagesize=report_layout['pagesize'])
        canvas.setTitle("analysis of video");
        self.lt=len(track.index)
        print "len="+str(self.lt)
        self.speed=speed
        self.report_layout=report_layout
        self.numpages=math.ceil(float(len(track.index))/(self.speed))
        leftmargin,bottommargin,rightmargin,topmargin=(1*cm,1*cm,1*cm,1*cm)
        ruler1height=1*cm
        ruler2height=1*cm
        L=report_layout['pagesize'][0]
        l=report_layout['pagesize'][1]
        self.L=L
        self.l=l
        self.track=track
        leftstart,bottomstart,rightend,topend=(leftmargin,bottommargin,L-rightmargin,l-topmargin)
        bottomstart+=ruler1height
        bottomstart+=ruler2height
        self.leftstart=leftstart
        self.hspace=rightend-leftstart
        self.vspace=topend-bottomstart
        ## compute outer boxes for each section
        totalweightsection=sum([s['layoutweight'] for s in report_layout['sections'] ])
        bw=0
        for s in self.report_layout['sections']:
            yb=self.vspace*bw/totalweightsection
            dy=(float(s['layoutweight'])*self.vspace)/totalweightsection
            bw+=float(s['layoutweight'])
            s['outerbox']=(leftstart,topend-yb-dy,self.hspace,dy)
        ## plan relations to innerbox
        for s in self.report_layout['sections']:
            (leftstart,botstart,dx,dy)=s['outerbox']
            s['innerbox']=(leftstart+(0.5*cm),botstart,dx-(0.5*cm),dy-(0.5*cm))
        self.do_page(-1,canvas)    
        for i in range(len(track[0])):
            print ("rendering details of subtrack %d of %d" % (i,len(track[0])))
            try: 
              self.subtrack_analysis(canvas, track,i)
            except Exception,e:
                print "Exception", str(e)
                pass
        for p in range(self.numpages):
            print ("rendering page %d of %d" % (p+1,self.numpages))
            self.do_page(p,canvas)
        canvas.save()
