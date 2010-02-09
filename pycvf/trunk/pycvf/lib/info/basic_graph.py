import numpy
import os
import sys
import random


def gentree(root, generators,depth):
    if (depth==0): return (root,None)
    r=map(lambda g:  gentree(g(root),generators,depth-1) ,generators)
    return (root,r)

def gentree2(root, generators,depth):
    if (depth==0): return {'node':root,'edges':[]}
    r=map(lambda g:  gentree2(g(root),generators,depth-1) ,generators)
    return {'node':root,'edges':r}


def explore_connected_graph(graph_root,node_edges, edge_target, visitor, node_func=lambda x:x,edge_func=lambda x,s,d:x):
    l=[graph_root]
    visitor.set_visited(graph_root)
    while (l!=[]):
        n=l.pop(0)
        node_func(n)
        for e in node_edges(n):
            #print e
            edge_func(e,n,edge_target(e))
        for newnode in map(edge_target,node_edges(n)):
            if (not visitor.has_visited(newnode)):
                visitor.set_visited(newnode)
                l.append(newnode)
    #visitid+=1

def rec_explore_connected_graph(graph_root,node_edges, edge_target, visitor, node_func=lambda x:x,edge_func=lambda x,s,d:x):
    l=[graph_root]
    visitor.set_visited(graph_root)
    while (l!=[]):
        n=l.pop()
        node_func(n)
        for e in node_edges(n):
            #print e
            edge_func(e,n,edge_target(e))
        for newnode in map(edge_target,node_edges(n)):
            if (not visitor.has_visited(newnode)):
                visitor.set_visited(newnode)
                l.append(newnode)

def explore_graph(graph_nodes,node_edges, edge_target, visitor, node_func=lambda x:x,edge_func=lambda x,s,d:x ):
    for n in graph_nodes:
        if (not visitor.has_visited(n)):
            explore_connected_graph(n,node_edges,edge_target, visitor, node_func,edge_func)


def int_maximal_connected_components(graph_nodes,node_edges,edge_target, visitor):
    class mcc_aglomerator:
        def __init__(self,n):
            self.g=[]
            self.cc=n
        def f(self,n):
            self.g.append(n)
    cc=0
    r=[]
    for n in graph_nodes:
        if (not visitor.has_visited(n)):
            mcc=mcc_aglomerator(cc)
            explore_connected_graph(n,node_edges,edge_target,visitor,node_func=mcc.f)
            r.append(mcc.g)
            cc+=1
    return r;


def _graph_to_tlp(graph_root,node_edges, edge_target,get_visitor, set_visited,node_info):
    buf=""
    class GiveIdAndCountExplorer:
        def __init__(self,idname='id'):
            self.idname=idname
            self.c=0
        def f(self,n,s=None,d=None):
            n[self.idname]=self.c
            self.c+=1
    giveid_and_count=GiveIdAndCountExplorer ()
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,giveid_and_count.f)
    buf+="(nodes "+' '.join(map(str,range(0,giveid_and_count.c)))+")\n"
    giveid_and_count_edges=GiveIdAndCountExplorer('eid')
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,edge_func=giveid_and_count_edges.f)
    class EdgePrintExplorer:
        def __init__(self,buf=""):
            self.buf=buf
        def f(self,e,s,d):
            self.buf+=("(edge %d %d %d)\n"%(e['eid'],s['id'],d['id']))
    ex=EdgePrintExplorer()
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,edge_func=ex.f)
    buf+=ex.buf
    buf+=("(property 0 size \"viewSize\"\n(default \"(5,5,5)\" \"(0.25,0.25,15)\")\n)\n")
    buf+="(property 0 string \"viewLabel\"\n(default \"\" \"\")"
    class NodeInfoExplorer:
        def __init__(self,nodeinfo,buf=""):
            self.buf=buf
            self.nodeinfo=nodeinfo
        def f(self,n):
            self.buf+=("(node %d \"%s\")\n"%(n['id'],str(self.nodeinfo(n))))
    ex=NodeInfoExplorer(node_info)
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,ex.f)
    buf+=ex.buf
    buf+=")"
    return buf;

def _graph_to_tlp2(graph_root,node_edges, edge_target,get_visitor,property_list):
    buf=""
    class GiveIdAndCountExplorer:
        def __init__(self,idname='id'):
            self.idname=idname
            self.c=0
        def f(self,n,s=None,d=None):
            n[self.idname]=self.c
            self.c+=1
    giveid_and_count=GiveIdAndCountExplorer ()
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,giveid_and_count.f)
    buf+="(nodes "+' '.join(map(str,range(0,giveid_and_count.c)))+")\n"
    giveid_and_count_edges=GiveIdAndCountExplorer('eid')
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,edge_func=giveid_and_count_edges.f)
    class EdgePrintExplorer:
        def __init__(self,buf=""):
            self.buf=buf
        def f(self,e,s,d):
            self.buf+=("(edge %d %d %d)\n"%(e['eid'],s['id'],d['id']))
    ex=EdgePrintExplorer()
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,edge_func=ex.f)
    buf+=ex.buf
    pid=0
    for p in property_list:
        buf+="(property "+str(pid)+" "+p['type']+" \""+p["name"]+"\"\n(default \""+p["default_node"]+"\" \""+p["default_edge"]+"\")"
        class PNodeExplorer:
            def __init__(self,nodeinfo=None,edgeinfo=None,buf=""):
                self.buf=buf
                self.nodeinfo=nodeinfo
                self.edgeinfo=edgeinfo
            def f(self,n):
                if (self.nodeinfo):
                    self.buf+=("(node %d \"%s\")\n"%(n['id'],str(self.nodeinfo(n))))
            def ef(self,e,s,d):
                if (self.edgeinfo):
                    self.buf+=("(edge %d \"%s\")\n"%(e['eid'],str(self.edgeinfo(e,s,d))))
        if (p.has_key('node_info') or p.has_key('edge_info')):
            buf+="\n"
            ex=PNodeExplorer(p.has_key('node_info') and p['node_info'] or None,  p.has_key('edge_info') and p['edge_info'] or None)
            visitor=get_visitor()
            explore_graph(graph_root,node_edges, edge_target,visitor,ex.f,ex.ef)
        buf+=ex.buf
        buf+=")\n"
        visitid+=1
        #pid+=1# tulip does not change this value actually
    return buf;

def _graph_to_dot(graph_root,node_edges, edge_target,get_visitor,property_list,name="thegraph"):
    buf="digraph "+name+"{"
    class GiveIdAndCountExplorer:
        def __init__(self,idname='id'):
            self.idname=idname
            self.c=0
        def f(self,n,s=None,d=None):
            n[self.idname]=self.c
            self.c+=1
    giveid_and_count=GiveIdAndCountExplorer ()
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,giveid_and_count.f)
    giveid_and_count_edges=GiveIdAndCountExplorer('eid')
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,edge_func=giveid_and_count_edges.f)
    class NodeEdgePrintExplorer:
        def __init__(self,plist=None,buf=""):
            self.buf=buf
            self.plist=plist
        def f(self,n):
            attrs=[]
            for p in property_list:
                if (p.has_key('node_info')):
                    x=p['node_info'](n)
                    if (x):
                        attrs.append(p['name']+'='+str(x))
            attrs=','.join(attrs)
            if (len(attrs)>0):
                self.buf+=("n%d [%s];\n"%(n['id'],attrs))
            else:
                self.buf+=("n%d;\n"%(n['id']))
        def ef(self,e,s,d):
            attrs=[]
            for p in property_list:
                if (p.has_key('edge_info')):
                    x=p['edge_info'](e,s,d)
                    if (x):
                        attrs.append(p['name']+'='+str(x))
            attrs=','.join(attrs)
            if (len(attrs)>0):
                self.buf+=("n%d->n%d [%s]\n"%(s['id'],d['id'],attrs))
            else:
                self.buf+=("n%d->n%d\n"%(s['id'],d['id']))
    ex=NodeEdgePrintExplorer(property_list)
    visitor=get_visitor()
    explore_graph(graph_root,node_edges, edge_target,visitor,ex.f,edge_func=ex.ef)
    buf+=ex.buf
    buf+="}\n"
    return buf;


#M1[dst,src]

def pseudomatprod(M1,M2,pplus=lambda x,y:x+y, pprod=lambda x,y:x*y,dtype=None,zeroval=0):
    if not dtype:
        dtype=M1.dtype
    i,j1=M1.shape
    j2,l=M2.shape
    assert(j1==j2)
    r=numpy.ndarray(shape=(i,l),dtype=dtype)
    r.fill(zeroval)
    r=numpy.matrix (r)
    for ii in range (i):
        for ll in range (l):
            for jj in range (j1):
                r[ii,ll]=pplus(r[ii,ll],pprod(M1[ii,jj],M2[jj,ll]))
    return r

def sqwm(dm):
    return pseudomatprod(wm,wm,pplus=max,pprod=lambda x,y:1./(1./x+1./y))

def sqdm(dm):
    return pseudomatprod(dm,dm,pplus=lambda x,y:min(x,y,key=abs),pprod=lambda x,y:x+y,zeroval=numpy.inf)

def mfixpoint(f,x0):
    px=x0
    nx=f(px)
    while sum(map(lambda x:((x!=0 ) and (not numpy.isnan(x))) and 1 or 0,(nx-px).flat)):
        px=nx
        nx=f(px)
        #print nx
        #print [x for x in (nx-px).flat]
    return nx
