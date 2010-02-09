# -*- coding: utf-8 -*-
import rpy

class RPyMultinomial():
    def __init__(self):
      self.pcv=None
    def train(self,obs,lab,maxobs=None):     
      eq=" + ".join([ "p%02d" %(i,) for i in range(obs.shape[1]) ]
		    +[ "I(p%02d * p%02d)" %(i,j) for i in range(obs.shape[1]) for j in range(i,obs.shape[1])  ]
		    +[ "I(p%02d * p%02d * p%02d)" %(i,j,k) for i in range(obs.shape[1]) for j in range(i,obs.shape[1]) for k in range(j,obs.shape[1]) ]  
		    )
      print "y ~ "+eq
      self.pc=None
      if (maxobs!=None):
        ro=range(obs.shape[0])
        random.shuffle(ro)
        obs=obs[ro]
        lab=lab[ro]
	linear_model = r.lm(r("y ~ "+eq), data = r.data_frame(**dict([("y",lab[:maxobs])]+[ ("p%02d" %(i,), obs[:maxobs,i]) for i in range(obs.shape[1]) ]  )) )
      else:
	linear_model = r.lm(r("y ~ "+eq), data = r.data_frame(**dict([("y",lab)]+[ ("p%02d" %(i,), obs[:,i]) for i in range(obs.shape[1]) ]  )) )
      print "COEFFICIENT=",filter(lambda x:(abs(x[1])>=0.001),linear_model["coefficients"].items())
      #print linear_model.keys()
      print "RESIDUAL=",linear_model["residuals"]
      #print dir(linear_model)
      self.lm=dict(filter(lambda x:x[0] in ["coefficients", "residuals"] ,linear_model.items()))
      self.pc=linear_model["coefficients"]
      self.pcv=numpy.array([self.pc[v] for v in [ "p%02d" %(i,) for i in range(obs.shape[1]) ]
		  +[ "I(p%02d * p%02d)" %(i,j) for i in range(obs.shape[1]) for j in range(i,obs.shape[1])  ]
		  +[ "I(p%02d * p%02d * p%02d)" %(i,j,k) for i in range(obs.shape[1]) for j in range(i,obs.shape[1]) for k in range(j,obs.shape[1])  ]
      ])
      self.pcv[numpy.isnan(self.pcv)]=0
      return self.pcv

__call__=RPyMultinomial
StatModel=RPyMultinomial

