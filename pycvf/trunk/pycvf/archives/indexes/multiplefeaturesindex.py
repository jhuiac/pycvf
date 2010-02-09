# -*- coding: utf-8 -*-

class MultipleFeaturesIndex():
    class FeatureIndex:
      def __init__(self,idx,enumeratef,recomposef0=None,recomposef1=None):
            self.enumeratef=enumeratef
            self.recomposef0=recomposef0
            self.recomposef1=recomposef1
            self.idx=idx
      def __del__(self):
         print "emfi"
      def enumerate(self,obj):
            return self.enumeratef(obj)
      def add(self,obj,*args,**kwargs):
            self.idx.add(self.enumeratef(obj),*args,**kwargs)
      def querymap(self,obj,dmap,*args,**kwargs):
            self.recomposef1(xmap,
                             self.model.getitem(self.enumeratef(obj), *args,**kwargs),
                            )
      def getballmap(self,obj,dmap,*args,**kwargs):
            self.recomposef1(xmap,
                             self.model.getball(self.enumeratef(obj), *args,**kwargs),
                            )
    def __init__(self,feature_indexes,topology_check_f=None):
      self.topology_check_f=topology_check_f
      self.feature_indexes=feature_indexes
    def __del__(self):
         print "emfi"
    def add(self,key,value,*args, ** kwargs):
      for c in self.feature_indexes:
         c.add(key,value,*args, ** kwargs) 
    def add_many(self,keys,values):
        self.add(keyx[k],values[k])
    def getitem(self,key,*args,**xargs):
       for c in self.feature_indexes:
         c.querymap(o,dmap,log=log,*args, ** kwargs) 
    def getball(self,key,*args,**xargs):
       for c in self.feature_indexes:
         c.getballmap(o,dmap,log=log,*args, ** kwargs) 


