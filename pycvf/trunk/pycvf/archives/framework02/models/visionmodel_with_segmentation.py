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

import re, os, math, random, time,sys, traceback,logging
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *
from pycvf.lib.info.graph import *

import visionmodel

def Grid2dGraph(gridsz,esc):     
    return Graph(gridsz,
		nodes_extract_f=(lambda g:numpy.ndindex(g)),  
		edges_extract_f=(lambda g:(map(lambda x:(x,(x[0],x[1]+1)), numpy.ndindex((g[0],g[1]-1))) 
					  +map(lambda x:((x[0],x[1]+1),x), numpy.ndindex((g[0],g[1]-1)))
					  +map(lambda x:((x[0]+1,x[1]),x), numpy.ndindex((g[0]-1,g[1])))
					  +map(lambda x:(x,(x[0]+1,x[1])), numpy.ndindex((g[0]-1,g[1])))    
				)),  
		node_outedges_f=(lambda g,n:(((n[0] >0 ) and [(n,(n[0]-1,n[1]))] or [])
					    +((n[0] <(g[0]-1) ) and [(n,(n[0]+1,n[1]))] or [])
					    +((n[1] <(g[1]-1) ) and [(n,(n[0],n[1]+1))] or [])
					    +((n[1] >0 ) and [(n,(n[0],n[1]-1))] or [])
					    )
				),  
		node_inedges_f=(lambda g,n:(((n[0] >0 ) and [((n[0]-1,n[1]),n)] or [])
					    +((n[0] <(g[0]-1) ) and [((n[0]+1,n[1]),n)] or [])
					    +((n[1] <(g[1]-1) ) and [((n[0],n[1]+1),n)] or [])
					    +((n[1] >0 ) and [((n[0],n[1]-1),n)] or [])
					    )
				),  
		edge_target_f=(lambda g,e:e[1]),   
		edge_source_f=(lambda g,e:e[0]),   
		edge_strength_f=(lambda g,e:esc(e)),    ###
		nodeid_f=(lambda g,n:n[0]+(n[1]*g[0])),   ###
		node_repr_f=(lambda g,n:repr(n)),
    )


def pt(a,b):
  return (a[0]+b[0],a[1]+b[1])

class MyModel(visionmodel.MyModel):
  def do_segmentation(self,probap,probah,probav,threshold,thesrc):
    R=(0,1)
    L=(0,-1)
    U=(1,0)
    D=(-1,0)
    #
    #v,h=probap.shape
    print probap.shape
    #
    eps=1e-24
    probah=probah+eps
    probav=probav+eps
    probap=probap+eps
    def edge_h_p(p):    
        #print "h", p, "/"  ,probah.shape , "/", probap.shape
	return min((probah[p]/probap[pt(p,R)]), (probah[p]/probap[p]))
    def edge_v_p(p):   
        #print "v", p, "/"  ,probav.shape , "/", probap.shape
	#print probav[p]
	return min((probav[p]/probap[pt(p,U)]), (probav[p]/probap[p]))
    def edge_u_p(p):
	return edge_v_p(p)
    def edge_d_p(p):   
	return edge_v_p(pt(p,D))
    def edge_l_p(p):
	return edge_h_p(pt(p,L))
    def edge_r_p(p):    
	return edge_h_p(p)
    def edgeweight(e):
        #print e
	dv=e[1][0]-e[0][0]
	dh=e[1][1]-e[0][1]
	if (dh):
	  if (dh>0):
	    return edge_r_p(e[0])
	  else:
	    return edge_l_p(e[0])
	else:
	  if (dv>0):
	    return edge_u_p(e[0])
	  else:
	    return edge_d_p(e[0])
    g=Grid2dGraph(probap.shape,edgeweight)
    sg=subgraph(g,filter(lambda e:(e.strength()>=threshold), g.edges()))
    print "computing maximal connected components"
    mccs=sg.maximal_connected_components()
    print "/computing maximal connected components"
    mccsc=(numpy.random.random(len(mccs),3)*255).astype(numpy.uint8)
    res=numpy.zeros(probap.shape+(3,),dtype=numpy.uint8)
    for mcci in range(len(mccs)):
	res[mccs[mcci]]=mccsc[mcci]
    #
    #
    import time
    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
    NumPy2PIL(res).save("/tmp2/segment-%s.png"%(time.time()))
    #
    #
    return res


  ## organize in a way we may use flood fill rather than mcc (graph framework is too slow that for)
  def do_khalimsky_segmentation(self,probap,probah,probav,threshold,thesrc):
    R=(0,1)
    L=(0,-1)
    U=(1,0)
    D=(-1,0)
    #
    #v,h=probap.shape
    print probap.shape
    #
    eps=1e-24
    probah=probah+eps
    probav=probav+eps
    probap=probap+eps
    def edge_h_p(p):    
        #print "h", p, "/"  ,probah.shape , "/", probap.shape
	return min((probah[p]/probap[pt(p,R)]), (probah[p]/probap[p]))
    def edge_v_p(p):   
        #print "v", p, "/"  ,probav.shape , "/", probap.shape
	#print probav[p]
	return min((probav[p]/probap[pt(p,U)]), (probav[p]/probap[p]))
    def edge_u_p(p):
	return edge_v_p(p)
    def edge_d_p(p):   
	return edge_v_p(pt(p,D))
    def edge_l_p(p):
	return edge_h_p(pt(p,L))
    def edge_r_p(p):    
	return edge_h_p(p)
    def edgeweight(e):
        #print e
	dv=e[1][0]-e[0][0]
	dh=e[1][1]-e[0][1]
	if (dh):
	  if (dh>0):
	    return edge_r_p(e[0])
	  else:
	    return edge_l_p(e[0])
	else:
	  if (dv>0):
	    return edge_u_p(e[0])
	  else:
	    return edge_d_p(e[0])
    res=numpy.ones((probap.shape[0]*2,probap.shape[1]*2),dtype=numpy.float)
    for p in numpy.ndindex(probap.shape):
      res[(p[0]*2+1,p[1]*2+1)]=0
    for p in numpy.ndindex((probap.shape[0]-1,probap.shape[1])):
      res[(p[0]*2+1,p[1]*2)]=edgeweight((p,(p[0]+1,p[1])))
    for p in numpy.ndindex((probap.shape[0],probap.shape[1]-1)):
      res[(p[0]*2,p[1]*2+1)]=edgeweight((p,(p[0],p[1]+1)))
    res=(res>=threshold)
    #
    #
    import time
    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
    NumPy2PIL(thesrc['src']).save("/tmp2/segment-id-%s.png"%(time.time()))
    NumPy2PIL(res.astype(numpy.uint8)*255).save("/tmp2/segment-%s.png"%(time.time()))
    #
    #
    return res
  def do_khalimsky_segdim(self,probap,probah,probav,threshold,thesrc):
    R=(0,1)
    L=(0,-1)
    U=(1,0)
    D=(-1,0)
    #
    #v,h=probap.shape
    print probap.shape
    #
    eps=1e-24
    probah=probah+eps
    probav=probav+eps
    probap=probap+eps
    def edge_h_p(p):    
        #print "h", p, "/"  ,probah.shape , "/", probap.shape
	return min((probah[p]/probap[pt(p,R)]), (probah[p]/probap[p]))
    def edge_v_p(p):   
        #print "v", p, "/"  ,probav.shape , "/", probap.shape
	#print probav[p]
	return min((probav[p]/probap[pt(p,U)]), (probav[p]/probap[p]))
    def edge_u_p(p):
	return edge_v_p(p)
    def edge_d_p(p):   
	return edge_v_p(pt(p,D))
    def edge_l_p(p):
	return edge_h_p(pt(p,L))
    def edge_r_p(p):    
	return edge_h_p(p)
    def edgeweight(e):
        #print e
	dv=e[1][0]-e[0][0]
	dh=e[1][1]-e[0][1]
	if (dh):
	  if (dh>0):
	    return edge_r_p(e[0])
	  else:
	    return edge_l_p(e[0])
	else:
	  if (dv>0):
	    return edge_u_p(e[0])
	  else:
	    return edge_d_p(e[0])
    res=numpy.ones((probap.shape[0]*2,probap.shape[1]*2),dtype=numpy.float)
    for p in numpy.ndindex(probap.shape):
      res[(p[0]*2+1,p[1]*2+1)]=0
    for p in numpy.ndindex((probap.shape[0]-1,probap.shape[1])):
      res[(p[0]*2+1,p[1]*2)]=edgeweight((p,(p[0]+1,p[1])))
    for p in numpy.ndindex((probap.shape[0],probap.shape[1]-1)):
      res[(p[0]*2,p[1]*2+1)]=edgeweight((p,(p[0],p[1]+1)))
    pres=(res>=threshold).astype(int)
    res=numpy.ones((probap.shape[0],probap.shape[1]),dtype=numpy.uint8)
    for p in numpy.ndindex(probap.shape):
      c=0
      if (p[0]-1>=0): 
         c+=pres[(p[0]*2-1,p[1]*2)]
      if (p[0]+1<probap.shape[0]): 
         c+=pres[(p[0]*2+1,p[1]*2)]
      if (p[1]-1>=0): 
         c+=pres[(p[0]*2,p[1]*2-1)]
      if (p[1]+1<probap.shape[1]): 
         c+=pres[(p[0]*2,p[1]*2+1)]
      res[p]=c
    
    #
    #
    import time
    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
    NumPy2PIL(thesrc['src']).save("/tmp2/segment-id-%s.png"%(time.time()))
    NumPy2PIL(res.astype(numpy.uint8)*63).save("/tmp2/segdim-%s.png"%(time.time()))
    #
    #
    return res

  def segment(self,basepath,trkfilename=None,threshold=0.9,patterntrack=None, edgehtrack=None, edgevtrack=None):
    ## we assume the last 3 features are in this order:
    ## pattern
    ##    edgeh
    ##    edgev
    for vr in self.vdb.all():   
      try:
	if (self.mode!="R"):
	  self.observed_features=[]
	  self.init_features()
	  self.init_observed_features_statistics(basepath=basepath,mlop="testv",mlargs="")
	  self.mode="R"
	  #vws_patterntrack=patterntrack or self.observed_features[-4]  
	  #vws_edgehtrack=edgehtrack or self.observed_features[-3]
	  #vws_edgevtrack=edgevtrack or self.observed_features[-2]
	  vws_patatrack=self.observed_features[-1][0]        
	  #
	  self.observed_features.append(
	     ('thesrc[vws_patatrack][0]',{'vws_patatrack':vws_patatrack},{})
	  )
	  print "vws_patatrack",vws_patatrack
	  self.observed_features.append(
	  #       'vws_do_segmentation(theimg[vws_patterntrack],theimg[vws_edgehtrack],theimg[vws_edgevtrack],vws_threshold)',
		('vws_do_segmentation(thesrc[vws_patatrack][0],thesrc[vws_patatrack][1],thesrc[vws_patatrack][2],vws_threshold,thesrc)',  
													  {
													    'vws_do_segmentation':self.do_khalimsky_segmentation,
													    #'vws_do_segmentation':self.do_khalimsky_segdim,
													    #'vws_patterntrack':vws_patterntrack,
													    #'vws_edgehtrack':vws_edgehtrack,
													    #'vws_edgevtrack':vws_edgevtrack,
													    'vws_patatrack':vws_patatrack,
													    'vws_threshold':threshold
													  },
		      {'title' : "segmentation"}  )
	    
	  )

	  if (trkfilename):
	    track=OnDiskMultiTrackLargeZ(filename=trkfilename,meta=map(lambda x: x[2],self.observed_features))
	  else:
	    track=NullTrack(meta=map(lambda x: x[2],self.observed_features))
        print "vws_patatrack",vws_patatrack	    
	self.videoreader=vr
	observer=MultipleObserver(map(lambda x:x[0],self.observed_features),track=track,context="jfli.project_specific.videoindex.videoprocessor")
	contextadd=reduce(lambda x,y:dict(zip(x.keys()+y.keys(),x.values()+y.values())),map(lambda x:x[1],self.observed_features),{})
	contextadd=dict(contextadd.keys()+self.add_ctx.keys(),contextadd.values()+self.add_ctx.values())
	observer.context=dict(zip(dir(observer.context)+contextadd.keys(),map(lambda x:eval("observer.context."+x,{"observer":observer}),dir(observer.context))+contextadd.values()))
	self.videoreader.set_observer(observer.iterproceed)
	self.videoreader.run()
	#self.observed_features=None
	observer.context=None
	observer=None
	self.videoreader=None
      except (Exception, RuntimeError),e:
          print "Exception during segmentation"
          print str(e)
          if (hasattr(sys,"last_traceback")):
            traceback.print_tb(sys.last_traceback)
          else:
            traceback.print_tb(sys.exc_traceback)       