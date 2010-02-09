## -*- coding: utf-8 -*-
## This is a small complement script to header2cython
##
## This file has been written by Bertrand NOUVEL
## Researcher at the JFLI
##
## Copyright CNRS  ## December 2008- April 2009
##
## ----------------------------------------------------------------------------

import re
import ctypeslib
import sys
import os
import numpy
import ctypes
import typedesc
import gccxmlparser
from smallgraph import *
try:
    import psyco
    psyco.full()
except:
    pass

opencvcython_disable_check=False

###############################################################################
## Architecture dependency
###############################################################################

if (ctypes.sizeof(ctypes.pointer(ctypes.c_int(0)))==4):
    POINTERTYPE="unsigned long"
elif (ctypes.sizeof(ctypes.pointer(ctypes.c_int(0)))==8):
    POINTERTYPE="unsigned long long"
else:
    raise Exception, "Unknown pointer size"

###############################################################################




###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################

def simplifyname(n):
    if (n[0:2]=='cv') and (('0'>n[2]) or ('9'<n[2])):
        t=n[2].lower()+n[3:]
	if t in [ "not" , "or", "and" ] :
	  return t+"_"
	return t
    else:
        return n

def highlevel_rename(n):
  #return MODULENAME+"_"+f.name
  return f.name    

def is_valid_pointer_on_structure(t,n):
  return (type(realtype_of(t))==typedesc.PointerType) and (type(realtype_of(realtype_of(t).typ))==typedesc.Structure) and (not (realtype_of(realtype_of(t).typ).name in INCOMPLETETYPES))


def is_valid_pointer_on_fundamental_type(t,n):
  return (type(realtype_of(t))==typedesc.PointerType) and (type(realtype_of(realtype_of(t).typ))==typedesc.FundamentalType)


def is_valid_pointer_on_structure_or_typedef_cv_arr(t,n):
   return (type(realtype_of(t))==typedesc.PointerType) and  (  (("name" in dir(no_const_type_of(realtype_of(t).typ))) and (no_const_type_of(realtype_of(t).typ).name=="CvArr")) 
                                                      or  (type(realtype_of(realtype_of(t).typ))==typedesc.Structure) and (not (realtype_of(realtype_of(t).typ).name in INCOMPLETETYPES)))





###################################################################################################################################################3
###################################################################################################################################################3
###################################################################################################################################################3



def classname_transform(n):
  return n

def pointerclassname_transform(n):
  return "PointerOn"+n



###
### These are all the rewrite rules that are used to make the syntax easier for the user.
###


REWRITE_RULES=\
[
 {  'rule_name': '__PointerOnImages',
    'declared_type_match': (lambda t,n:  (is_valid_pointer_on_structure(t,n) and (realtype_of(realtype_of(t).typ).name in ["UIplImage"]))),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         { ## numpy arrays 
           'match_expr': (lambda t,n:"type("+n+")==numpy.ndarray"),
           'returns': (lambda t,n:"zopencv_core.NumPy2IplFast("+n+").get_pointer()")
         },
         { ## wrapper Types
           'match_expr': (lambda t,n: "(type("+n+")==zopencv_classes."+classname_transform(realtype_of(realtype_of(t).typ).name)+") or (type("+n+")==zopencv_pclasses."+pointerclassname_transform(realtype_of(realtype_of(t).typ).name)+")" ),
           'returns': (lambda t,n:n+".get_pointer()")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')
	  'returns': (lambda t,n:'('+n+')')	  	  
	 }
     ]
  },
  { 'rule_name': '__PointerOnMatrices',
    'declared_type_match': (lambda t,n:  (is_valid_pointer_on_structure(t,n) and (realtype_of(realtype_of(t).typ).name in ["CvMat"]))),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         { ## numpy arrays 
           'match_expr': (lambda t,n:"type("+n+")==numpy.ndarray"),
           'returns': (lambda t,n:"zopencv_core.NumPy2CvMatFast("+n+").get_pointer()")
         },
         { ## wrapper Types
           'match_expr': (lambda t,n: "(type("+n+")==zopencv_classes."+classname_transform(realtype_of(realtype_of(t).typ).name)+") or (type("+n+")==zopencv_pclasses."+pointerclassname_transform(realtype_of(realtype_of(t).typ).name)+")" ),
           'returns': (lambda t,n:n+".get_pointer()")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')
	  'returns': (lambda t,n:'('+n+')')	  	  
	 }
     ]
  },
  { 'rule_name': '__PointerOnNDMatrices',
    'declared_type_match': (lambda t,n:  (is_valid_pointer_on_structure(t,n) and (realtype_of(realtype_of(t).typ).name in ["CvMatND"]))),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         { ## numpy arrays 
           'match_expr': (lambda t,n:"type("+n+")==numpy.ndarray"),
           'returns': (lambda t,n:"zopencv_core.NumPy2CvMatNDFast("+n+").get_pointer()")
         },
         { ## wrapper Types
           'match_expr': (lambda t,n: "(type("+n+")==zopencv_classes."+classname_transform(realtype_of(realtype_of(t).typ).name)+") or (type("+n+")==zopencv_pclasses."+pointerclassname_transform(realtype_of(realtype_of(t).typ).name)+")" ),
           'returns': (lambda t,n:n+".get_pointer()")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')
	  'returns': (lambda t,n:'('+n+')')	  	  
	 }
     ]
  },
  { 'rule_name': '__PointerOnPoints', 
    'declared_type_match': (lambda t,n:  (is_valid_pointer_on_structure(t,n) and (realtype_of(realtype_of(t).typ).name in ["CvPoint"]))),
    'instantiated_type_match': [
         { ## numpy arrays 
           'match_expr': (lambda t,n:"type("+n+")==numpy.ndarray"),
           'returns': (lambda t,n:"zopencv_core.zopencv_highlevel.cvPoint("+n+"[0],"+n+"[1])")
         },
         { ## tuple
           'match_expr': (lambda t,n:"(type("+n+") in [ tuple, list] and (len("+n+"==2)))"),         
           'returns': (lambda t,n:"zopencv_core.zopencv_highlevel.cvPoint("+n+"[0],"+n+"[1])")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')
	  'returns': (lambda t,n:'('+n+')')	  	  
	 }
     ]
  },  
  { 'rule_name': '__PointerOnCvArr', 
    'declared_type_match': (lambda t,n:  ((is_valid_pointer_on_fundamental_type(t,n) 
                                    and (hasattr(no_const_type_of(realtype_of(t).typ),"name") and no_const_type_of(realtype_of(t).typ).name in ["CvArr"])))),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         { ## numpy arrays 
           'match_expr': (lambda t,n:"type("+n+")==numpy.ndarray"),
           'returns': (lambda t,n:"zopencv_core.NumPy2IplFast("+n+").get_pointer()")
         },
	 { ## wrapper Types
	   'match_expr': (lambda t,n: "(type("+n+") in [ "+','.join(map(lambda xx:"zopencv_classes."+xx,["UIplImage","CvMat"]))+" ] ) or (type("+n+")in [ "+','.join(map(lambda xx:"zopencv_pclasses."+pointerclassname_transform(xx), ["UIplImage","CvMat"]))+" ] )" ) ,
           'returns': (lambda t,n:n+".get_pointer()")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')	  
           'returns': (lambda t,n:'('+n+')')	  	  
	 }
     ]
  },
  { ## pointers declared
    'rule_name': '__PointerOnDeclaredClass',
    'declared_type_match': (lambda t,n: (is_valid_pointer_on_structure(t,n) and(realtype_of(realtype_of(t).typ).name in declaredstructlist))),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         {
                 'match_expr': (lambda t,n: "(type("+n+")==zopencv_classes."+classname_transform(realtype_of(realtype_of(t).typ).name)+") or (type("+n+")==zopencv_pclasses."+pointerclassname_transform(realtype_of(realtype_of(t).typ).name)+")" ),
                 'returns': (lambda t,n:n+".get_pointer()")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')	  
           'returns': (lambda t,n:'('+n+')')	  	  
	 }
       ]
  },
  {  'rule_name': '__PointerOnOtherStructure',
     'declared_type_match': (lambda t,n:  (is_valid_pointer_on_structure(t,n))),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         { ## wrapper Types
           'match_expr': (lambda t,n: "hasattr("+n+",'get_pointer')" ),
           'returns': (lambda t,n:n+".get_pointer()")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')	  
           'returns': (lambda t,n:'('+n+')')	  	  
	 }
     ]
  },

  { ## pointers on fundamental types 
    'rule_name': '__PointerOnFundamentalType',
    'declared_type_match': (lambda t,n:is_valid_pointer_on_fundamental_type(t,n)),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"((type("+n+")==int) or (type("+n+")==long))"),
           'returns': (lambda t,n:n)
         },
         { ## numpy arrays 
           'match_expr': (lambda t,n:"type("+n+")==numpy.ndarray"),
           'returns': (lambda t,n:"(<"+POINTERTYPE+">PyArray_DATA("+n+"))")
         },
         { ## strings
           'match_expr': (lambda t,n:"type("+n+")==str"),
           'returns': (lambda t,n:"(<"+POINTERTYPE+">zopencv_core.str_addr("+n+"))")
         },
	 { ## error
           'match_expr': (lambda t,n:"True"),
           'returns': (lambda t,n:'('+n+')')	  	  
           #'returns': (lambda t,n:'('+n+'/INVALID_TYPE_ERROR)')	  
	 }

    ]
  },
  { ## default match
    'rule_name': '__RawArgument',
    'declared_type_match': (lambda t,n:True),
    'instantiated_type_match': [
         {  ## raw pointers
           'match_expr': (lambda t,n:"True"),
           'returns': (lambda t,n:n),
         },
    ]
  }

]






declaredstructlist=[]

METHPREFIX="raw__"
METHPREFIX=""

MODULENAME="cv"

INCOMPLETETYPES=os.environ['INCOMPLETETYPES'].split(" ")
EXPLICITTYPES=os.environ['EXPLICITTYPES'].split(" ")
IGNOREFUNCTIONS=os.environ['IGNOREFUNCTIONS'].split(" ")
includes=os.environ["FILES"].split(" ")

###############################################################################
#xcvsym=query_items("cvall.xml")


################################################################################
def decld(n):
  """ this function is used to access the declaration module"""
  return n
################################################################################




###############################################################################
def realtype_of(t):
    """ we are not intersted in syntactic sugar"""
    if (type(t)==typedesc.Typedef):
        return realtype_of(t.typ)
    if (type(t)==typedesc.CvQualifiedType):
        return realtype_of(t.typ)
    else:
        return t

###############################################################################
def no_const_type_of(t):
    """ as cython we forget about "const" """
    if (type(t)==typedesc.CvQualifiedType):
        return no_const_type_of(t.typ)
    else:
        return t




###############################################################################
def ctypestr(t):
    """ writes a type in way cython expect a Ctype declaration """
    if (type(t)==typedesc.FunctionType):
        return "void *"
    if (type(t)==typedesc.PointerType):
        return ctypestr(t.typ)+" *"
    if (type(t)==typedesc.ArrayType):
        return ctypestr(t.typ)+" *"
    try:
        if type(t) in [ typedesc.Structure , typedesc.Typedef ]:
	  n=decld(t.name)
	else:
	  n=t.name
        return n
    except:
        #sys.stderr.write(str(dir(t))+"\n")
        return ctypestr(t.typ)

###############################################################################
def argprintstr(t,n,altcast=None):
    """ used to pass arguments to a function when we call it... obviously casts are sometime necessary  """
    if (type(t)==typedesc.PointerType) or (type(t)==typedesc.ArrayType) :
        return "<"+ ctypestr(t) + ">"+n
    if (type(t)==typedesc.Typedef):
        try:
            if ( ((type(rt(t.typ))==typedesc.PointerType) and (type(rt(t.typ).typ)==typedesc.FunctionType)  ) or (t.typ.name!=t.name)):
                return "<"+ decld(t.name) + "> "+argprintstr(t.typ,n)
        except:
            pass
        return argprintstr(t.typ,n)
    elif (type(t)==typedesc.Enumeration):
                return "<"+ decld(t.name) + "> "+n
    elif (type(t)==typedesc.Structure):
        if (altcast):
            return "(<typeof("+decld(altcast)+")*><"+POINTERTYPE+">"+n+".get_pointer())[0]"
        else:
            return "(<"+decld(t.name)+"*><"+POINTERTYPE+">"+n+".get_pointer())[0]"
    else:
        return n


###############################################################################
def rawctypestr(t):
    """ what is the basic name of the object behind this type... """
    global POINTERTYPE
    if (type(t)==typedesc.PointerType):
        return POINTERTYPE
    if (type(t)==typedesc.ArrayType):
        return POINTERTYPE
    if (type(t)==typedesc.FunctionType):
        return POINTERTYPE
    if (type(t)==typedesc.Enumeration):
        return "int"
    if (type(t)==typedesc.Structure):
        return "object"
#"MODULENAME+"_"+f.name
    if (type(t)==typedesc.Typedef):
        return rawctypestr(t.typ)
    try:
        if type(t) in [ typedesc.Structure , typedesc.Typedef, typedesc.Enumeration]:
	  n=decld(t.name)
	else:
	  n=t.name
        return n
    except:
        #sys.stderr.write(str(dir(t))+"\n")
        return ctypestr(t.typ)

###############################################################################
def irawctypestr(t):
    global POINTERTYPE
    rtt=realtype_of(t)
    if (type(rtt)==typedesc.PointerType) or (type(rtt)==typedesc.ArrayType):
        return "<"+POINTERTYPE+">"
    return ""

###############################################################################
def try_match_location(includef,x):
    try:
        return includef==(x.location[0].split("/")[-1])
    except:
        return False

###############################################################################
def try_match_location_in(includefl,x):
    try:
        return (x.location[0].split("/")[-1]) in includefl
    except:
        return False

def required_subtypes(t):
    if (type(t)==typedesc.Structure):
        return [t]
    if (type(t)==typedesc.Union):
        return [t]
    elif (type(t)==typedesc.Typedef):
        return [t]
    elif (type(t)==typedesc.FundamentalType):
        return []
    elif (type(t)==typedesc.Enumeration):
        return []
    elif (type(t)==typedesc.PointerType):
        return required_subtypes(t.typ)
    elif (type(t)==typedesc.CvQualifiedType):
        return required_subtypes(t.typ)
    elif (type(t)==typedesc.ArrayType):
        return required_subtypes(t.typ)
    elif (type(t)==typedesc.FunctionType):
        r=required_subtypes(t.returns)
        for e in t.iterArgTypes():
            r.extend(required_subtypes(e))
        return r
    else:
        raise Exception, "Unhandled"+str(type(t))+str(dir(t))+str(t)


###############################################################################
## Here we create a graph of all the dependencies in-between types in order to
## to declare the types in a valid order
###############################################################################


def _create_typegraph(nodes,edges,n,rn=None,st=[]):
    if not rn:
        rn=n
    if n in st:
        sys.stderr.write("looping reqtypes for "+n.name+" (fixup required!)\n")
        assert(0)
    st.append(n)
    if type(n)==typedesc.Typedef:
        for rt in required_subtypes(n.typ):
            if (rn!=rt) and ((not 'name' in dir(rt)) or rt.name  not in INCOMPLETETYPES):
                edges.append((rt,rn))
    elif type(n)==typedesc.Structure:
        for m in n.members:
            if ( type(n)==typedesc.Field):
                for rt in required_subtypes(m.typ):
                    if (rn!=rt) and ((not 'name' in dir(rt)) or rt.name  not in INCOMPLETETYPES):
                        edges.append((rt,rn))
            else:
                _create_typegraph(nodes,edges,m,rn,st)
                #if len (kx):
                #  print kx
                #  edges.extend(kx)
    elif type(n)==typedesc.Union:
        for m in n.members:
            if ( type(n)==typedesc.Field):
                for rt in required_subtypes(m.typ):
                    if (rn!=rt) and ((not 'name' in dir(rt)) or rt.name not in INCOMPLETETYPES):
                        edges.append((rt,rn))
            else:
                _create_typegraph(nodes,edges,m,rn,st)
                #if len (kx):
                #  print kx
                #  edges.extend(kx)
    elif type(n)==typedesc.Field:
        for rt in required_subtypes(n.typ):
            if (rn!=rt) and ((not 'name' in dir(rt)) or rt.name not in INCOMPLETETYPES):
                edges.append((rt,rn))
    elif type(n)==typedesc.Ignored:
        pass
    else:
        sys.stderr.write( "error with %s" %(str(n)) )
        assert(0)
    st.pop()
    return edges

def create_typegraph():
    nodes=filter(
      lambda x:
	try_match_location_in(includes,x) 
	and 
        (type(x)==typedesc.Structure  
          or (type(x)==typedesc.Union or type(x)==typedesc.Typedef ) 
          and ((not 'name' in dir(realtype_of(x))) or x.name not in INCOMPLETETYPES)
        ) ,list(xcvsym[0]))
    edges=[]
    nodes.reverse()
    for n in nodes:
    #sys.stderr.write(n.name+"\n")
        edges=_create_typegraph(nodes,edges,n,n)
    edges=list(set(edges))
    for e in edges:
        if not e[0] in nodes:
            nodes.append(e[0])
        if not e[1] in nodes:
            nodes.append(e[1])
    return nodes,edges


###############################################################################
def declprintstr(t,n):
    if (t==typedesc.ArrayType):
        M=t.max
        mi=t.min
        if (M[-1]=='u'): M=M[:-1]
        if (mi[-1]=='u'): mi=mi[:-1]
        M=int(M)
        mi=int(mi)
        return declprintstr(t.typ,n)+"["+str(M-mi)+ "]"
    else:
        return ctypestr(t)+ " "+n


def write_struct_union_members_accessors(listelems,prefix=[],outfile=None):
    for m in listelems:
        if (not m.name):
            continue
        pn=prefix+[m.name]
        mt=type(realtype_of(m))
        if (mt!=typedesc.Union) and (mt!=typedesc.Structure):
            if (mt==typedesc.Field):
                mtt=type(realtype_of(realtype_of(m).typ))
                if (mtt!=typedesc.Union) and (mtt!=typedesc.Structure):
                    outfile.write( "\tproperty "+METHPREFIX+'_'.join(pn)+":\n")
                    #sys.stderr.write(str(type(m))+","+str(mt)+"\n")
                    mttt=realtype_of(realtype_of(m).typ)
                    outfile.write( "\t#"+str(mtt)+","+str(mttt)+"\n")
                    outfile.write( "\t\tdef __set__(self,"+rawctypestr(mttt)+" value):\n")
                    if (mtt!=typedesc.ArrayType):
                        outfile.write( "\t\t\tself.instance."+'.'.join(pn)+"="+argprintstr(realtype_of(m).typ,"value")+"\n") #,"self.instance."+'.'.join(pn))
                    else:
                        idx=[]
                        xmttt=mttt
                        while (type(xmttt)==typedesc.ArrayType):
                            M=xmttt.max
                            mi=xmttt.min
                            if (M[-1]=='u'): M=M[:-1]
                            if (mi[-1]=='u'): mi=mi[:-1]
                            mi=int(mi)
                            M=int(M)
                            if not (M-mi):
                                outfile.write( "\t\t\tpass\n")
                                continue
                            xmttt=realtype_of(xmttt.typ)
                            idx.append(M-mi)
                        #"self.instance."+'.'.join(pn)+"["+str(i)+"]
                        if (type(xmttt)==typedesc.Structure):
                            outfile.write( "\t\t\tmemcpy(<void *>self.instance."+'.'.join(pn)+",<void *><"+POINTERTYPE+">value,sizeof("+decld(xmttt.name)+")*" + str(reduce(lambda x,y:x*y,idx,1)) + ")\n")
                        else:
                            for i in numpy.ndindex(tuple(idx)):
                                outfile.write( "\t\t\tself.instance."+'.'.join(pn)+"["+("][".join(map(str,i)))+"]=("+argprintstr(realtype_of(m).typ,"value")+")["+("][".join(map(str,i)))+"]\n")
                    outfile.write( "\t\tdef __get__(self):\n")
                    #if mtt=
                    outfile.write( "\t\t\treturn "+ irawctypestr(mttt)  +"self.instance."+'.'.join(pn)+"\n")
                else:
                    if (mtt==typedesc.Structure):
                        outfile.write( "\tproperty "+METHPREFIX+'_'.join(pn)+":\n")
                        outfile.write( "\t\tdef __set__(self, value):\n")
                        outfile.write( "\t\t\tif ((type(value)!=long)and(type(value)!=int)):\n")
                        outfile.write( "\t\t\t\tvalue=value.get_pointer()\n")
                        outfile.write( "\t\t\tmemcpy(<void *>& self.instance."+'.'.join(pn)+",<void *><"+POINTERTYPE+">value,sizeof("+decld(realtype_of(m.typ).name)+"))\n")
                        outfile.write( "\t\tdef __get__(self):\n")
                        outfile.write( "\t\t\treturn zopencv_pclasses."+pointerclassname_transform(realtype_of(m.typ).name)+"(<"+POINTERTYPE+">&self.instance."+'.'.join(pn)+")\n")
                    write_struct_union_members_accessors(realtype_of(m.typ).members,pn,outfile=outfile)
            else:
                sys.stderr.write(str(mt)+" union/structure/ pseudofield ignored \n")
        else:
            if (m.name==m.struct_head.struct.name):
                continue
            #sys.stderr.write(str(m.__dict__)+"...\n")
            write_struct_union_members_accessors(m.members,pn,outfile=outfile)
            #sys.stderr.write("forgetting structure union for the moment (in "+f.name+")...\n")
            outfile.write( "\t\tdef __set__(self, value):\n")
            outfile.write( "\t\t\tif (type(value)=="+POINTERTYPE+"):\n")
            outfile.write( "\t\t\tmemcpy(<void *>self.instance."+'.'.join(pn)+",<void *><"+POINTERTYPE+">value,sizeof("+decld(xmttt.name)+"))\n")
        outfile.write("\n")



def write_struct_union_members_accessors2(listelems,prefix=[]):
    for m in listelems:
        if (not m.name):
            continue
        pn=prefix+[m.name]
        mt=type(realtype_of(m))
        if (mt!=typedesc.Union) and (mt!=typedesc.Structure):
            if (mt==typedesc.Field):
                mtt=type(realtype_of(realtype_of(m).typ))
                if (mtt!=typedesc.Union) and (mtt!=typedesc.Structure):
                    print "\tproperty "+'_'.join(pn)+":"
                    mttt=realtype_of(realtype_of(m).typ)
                    print "\t#"+str(mtt)+","+str(mttt)
                    print "\t\tdef __set__(self,"+rawctypestr(mttt)+" value):"
                    if (mtt!=typedesc.ArrayType):
                        print "\t\t\tself.instance."+'.'.join(pn)+"="+argprintstr(realtype_of(m).typ,"value") #,"self.instance."+'.'.join(pn))
                    else:
                        print "\t\t\tif (type(value)==)"
                        print "\t\t\tsuper("++")"
                    print "\t\tdef __get__(self):"
                    #if mtt=
                    print "\t\t\treturn "+ irawctypestr(mttt)  +"self.instance."+'.'.join(pn)
                else:
                    write_struct_union_members_accessors(realtype_of(m.typ).members,pn)
            else:
                sys.stderr.write(str(type(mt))+" ignored \n")
        else:
            if (m.name==m.struct_head.struct.name):
                continue
            sys.stderr.write(str(m.__dict__)+"...\n")
            write_struct_union_members_accessors(m.members,pn)



############################################################################################################################################################################
############################################################################################################################################################################
### Here we write function for higher level methods
############################################################################################################################################################################
############################################################################################################################################################################



def correctarg(t,n):
    """ this function is called on each argument in order to add the proper workaround for it to be bassed correctly and safely to the C function """
    for tsr in REWRITE_RULES:
      if (tsr["declared_type_match"](t,n)):
	return ' or '.join( [ "((" +r["match_expr"](t,n) + ") and "+r["returns"](t,n) + ")"  for r in tsr["instantiated_type_match"] ]   )

def correctargb(t,n):
    """ this function is called on each argument in order to add the proper workaround for it to be bassed correctly and safely to the C function """
    for tsr in REWRITE_RULES:
      if (tsr["declared_type_match"](t,n)):
	return ' or '.join( [ "((" +r["match_expr"](t,n) + ") and "+r["returns"](t,n) + ")"  for r in tsr["instantiated_type_match"] ]   )


def old_correctarg(t,n):
    if (is_valid_pointer_on_structure(t,n)):
        stt=realtype_of(realtype_of(t).typ)
        if (stt.name=="UIplImage" or stt.name=="UIplImage"  or stt.name=="CvMat"  or stt.name=="CvArr"):
            return "((((type("+n+")==int) or (type("+n+")==long))  and "+ n +") or((type("+n+")==numpy.ndarray) and (NumPy2IplFast("+n+").get_pointer()) " \
		+ "or  ( "+wrap_get_pointer_on_declared_type_or_pointer(t,n) +")" \
		+reduce(lambda b,tname:b+"or  ( "+wrap_get_pointer_on_explict_type(tname,n) +")",["UIplImage","CvMat"],"")
        else:
            return "((((type("+n+")==int) or (type("+n+")==long))  and "+ n +") or ( "+ wrap_get_pointer_on_declared_type_or_pointer(t,n)
    elif is_valid_pointer_on_fundamental_type(t,n):
        return "((type("+n+")==numpy.ndarray) and (<"+POINTERTYPE+">PyArray_DATA("+n+")) or "+n+")"
        #return "((type("+n+")==numpy.ndarray) and ( memory_addr_of_numpy_array ( "+n+"))"
    else:
        return n




def xhas_attr(o,s):
    try:
        eval("o."+s,{o:o})
        return True
    except:
        return False

def export_methods(zzinc,typestruct,prefixmodule=""):
    """ write highlevel  accessors to methods """
    for includef in includes:
        for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
            if ((type(f)==typedesc.Function) and (not (f.name in IGNOREFUNCTIONS))):
                try:
                    bt=f.iterArgTypes().next()
                except:
                    continue
                if (bt==typestruct):
                    zzinc.write( "\tdef "+ simplifyname(f.name)+ "(self,"+ ','.join(map(lambda x:"arg_"+x,f.iterArgNames())[1:]) + "):\n")
                    zzinc.write( "\t\treturn "+prefixmodule+"zopencv_lowlevel._raw_"+f.name+'(self,' + ','.join(map(lambda x:correctarg(x[0],"arg_"+x[1]),zip(f.iterArgTypes(), f.iterArgNames())[1:])) + ')\n')
                elif ((type(bt)==typedesc.PointerType) and ( (realtype_of(bt.typ)==typestruct)
                or ((type(realtype_of(bt.typ))==typedesc.Union) and (typestruct in  map(lambda t:t.typ,realtype_of(bt.typ).members))) or ( typestruct.name=="_IplImage" or typestruct.name=="UIplImage"  or typestruct.name=="CvMat" and xhas_attr(bt.typ,'name') and (bt.typ.name=="CvArr")) )):
                    zzinc.write( "\tdef "+simplifyname(f.name)
      + "(self,"+ ','.join(map(lambda x:"arg_"+x,f.iterArgNames())[1:]) + "):\n")
                    zzinc.write( "\t\treturn "+prefixmodule+"zopencv_lowlevel._raw_"+f.name+'(self.get_pointer(),' + ','.join(map(lambda x:correctarg(x[0],"arg_"+x[1]),zip(f.iterArgTypes(), f.iterArgNames())[1:])) + ')\n')

def export_methods2(zzinc,typestruct,prefixmodule=""):
    for includef in includes:
        for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
            if ((type(f)==typedesc.Function) and (not (f.name in IGNOREFUNCTIONS))):
                try:
                    bt=f.iterArgTypes().next()
                except:
                    continue
                if (bt==typestruct):
                    zzinc.write( "\tdef "+ simplifyname(f.name)+ "(self,"+ ','.join(map(lambda x:"arg_"+x,f.iterArgNames())[1:]) + "):\n")
                    zzinc.write( "\t\treturn self.instance."+simplifyname(f.name)+'('+ ','.join(["arg_"+tt for tt in f.iterArgNames()][1:]) + ')\n')



def decl_structuniontyped(out,f,baseindent="\t"):
    if ((type(f)==typedesc.Structure)) or ((type(f)==typedesc.Union)):
        for m in f.members:
            if (type(m)==typedesc.Union):
                decl_structuniontyped(out,m,baseindent)
            if (type(m)==typedesc.Structure):
                decl_structuniontyped(out,m,baseindent)
        out.write( baseindent+(baseindent =="\t" and "cdef " or "" )+"struct "+(baseindent =="\t" and f.name or "" )+":\n")
        empty=True
        for m in f.members:
            if (type(m)==typedesc.Field):
                if (m.name):
                    out.write( baseindent+"\t"+ctypestr(m.typ)+" "+m.name+"\n")
                    empty=False
            elif (type(m)==typedesc.Union):
                #decl_structuniontyped(m,baseindent+"\t")
                out.write( baseindent+"\t"+m.name + " _"+m.name+"\n")
                empty=False
            elif (type(m)==typedesc.Structure):
                #decl_structuniontyped(m,baseindent+"\t")
                out.write( baseindent+"\t"+ m.name + " _"+m.name+"\n")
                empty=False
        if empty:
            out.write( baseindent+"\tpass\n")
    elif ((type(f)==typedesc.Union)):
        print baseindent+(baseindent =="\t" and "cdef " or "" )+"union "+(baseindent =="\t" and f.name or "" )+":"
        for m in f.members:
            if (m.name):
                out.write( baseindent+"\t"+ctypestr(m.typ)+" "+m.name+"\n")
    elif ((type(f)==typedesc.Typedef)):
        out.write(baseindent+"ctypedef "+ctypestr(f.typ)+" "+f.name+"\n")
    #elif ((type(f)==typedesc.Typedef)):
    #  print(baseindent+"ctypedef "+ctypestr(f.typ)+" "+f.name)





######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
## main process
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
xcvsym=(gccxmlparser.parse("cvall.xml"),[],[])

sys.stderr.write( ":".join(includes) +"\n")
sys.stderr.write( "INCOMPLETETYPES="+ ":".join(INCOMPLETETYPES)+"\n")
sys.stderr.write( "IGNOREFUNCTIONS="+ ":".join(IGNOREFUNCTIONS)+"\n")



headersupp=open("suppheaders.i","w")
for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Structure) and (not (f.name in INCOMPLETETYPES))):
            try:
                f.name.index("DOT")
                headersupp.write("typedef struct "+f.name+" {\n")
                for m in f.members:
                    if (type(m)==typedesc.Ignored):
                        continue
                    xx=realtype_of(realtype_of(m).typ)
                    if (type(xx)==typedesc.ArrayType):
                        assert(0)
                    if (type(xx)==typedesc.FunctionType):
                        assert(0)
                    if (type(xx)==typedesc.Ignored):
                        continue
                    headersupp.write("\t"+declprintstr(m.typ,m.name)+";\n")
                headersupp.write("int export_magic[0];")
                headersupp.write("} "+f.name+"_t;\n\n")
            except ValueError:
                pass
            try:
                f.name.index("DOLLAR")
                headersupp.write("typedef struct "+f.name+" {\n")
                for m in f.members:
                    if (type(m)==typedesc.Ignored):
                        continue
                    xx=realtype_of(realtype_of(m).typ)
                    if (type(xx)==typedesc.ArrayType):
                        assert(0)
                    if (type(xx)==typedesc.FunctionType):
                        assert(0)
                    if (type(xx)==typedesc.Ignored):
                        continue
                    headersupp.write("\t"+declprintstr(m.typ,m.name)+";\n")
                headersupp.write("int export_magic[0];")
                headersupp.write("} "+f.name+"_t;\n\n")
            except ValueError:
                pass

#
headersupp.close()


###################################################################################################
## These basic functions depends on POINTERTYPE However they should be diverted in some other file
##################################################################################################



cythonfile1=sys.stdout
cythonfile1.write(re.subn("%POINTERTYPE%",POINTERTYPE,file("header_template.pyx").read())[0])


def new_cython_file(filename):
     f=open(filename,"w")
     f.write(re.subn("%POINTERTYPE%",POINTERTYPE,file("header_generic.pyx").read())[0])
     return f

def new_cython_decl_file(filename):
     f=open(filename,"w")
     f.write(re.subn("%POINTERTYPE%",POINTERTYPE,file("header_generic.pxd").read())[0])
     return f

########################################################################################################################3
### Here we effectively create the typegraph
########################################################################################################################3

g=create_typegraph()
#sys.stderr.write(str(g[0]))
if False:
    G=graph_node_edge_lists(g,xnode_repr_f=lambda n:type(n).__name__+"_"+n.name)
    gf=file("typegraph.dot","w")
    gf.write(G.quick_dot_string())
    gf.close()
    #G.quick_dot_show()
else:
    G=graph_node_edge_lists(g)

#try:
tpg=map(lambda x:x.bo,topological_sort(G))
#except:
#  sys.stderr.write("ignoring topological sort / may work due to declaration files")
#  tpg=g[0]#G.nodes()
  

gfx=file("typegraph.txt","w")
gfx.write( "\n".join(map(lambda x:x.name,tpg)))
gfx.close()



##########################################################################################
# Declaration of the functions and of the types
#########################################################################################

################################################################################
def decld(n):
  return n
################################################################################


zzdcl=open("declarations.pxd","w")
zzdcl.write(file("declarations_header.pyx").read())
zzdcl.write("cimport numpy\n")
zzdcl.write("cimport stdlib\n")
zzdcl.write("ctypedef stdlib.size_t size_t\n")

for t in INCOMPLETETYPES:
 if t not in EXPLICITTYPES:
   if (len(t)):
    zzdcl.write( "ctypedef void %s\n"%(t))
zzdcl.write( "\n")

#print "cdef extern from '%s':"%("cvall.h")
for includef in includes:
    zzdcl.write( "cdef extern from '%s':\n"%(includef))
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        try:
            if ((type(f)==typedesc.Enumeration)):
                zzdcl.write( "\tcdef enum "+f.name+":\n")
                for sf in f.values:
                    if (type(sf)==typedesc.EnumValue):
                        zzdcl.write("\t\t"+sf.name+"="+str(sf.value)+"\n")
                zzdcl.write( "\t\n")
        except:
            pass
    for f in filter(lambda x:try_match_location(includef,x),tpg):
        decl_structuniontyped(zzdcl,f)
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Function)):
            zzdcl.write( "\t"+ctypestr(f.returns)+" "+ f.name+"("+  ",".join(map(lambda x:(ctypestr(x[0])+ " "+x[1])  , zip(f.iterArgTypes(),f.iterArgNames()))) +")\n")
    zzdcl.write( "\n")

zzdcl.write( "cdef extern from 'suppheaders.i':\n\n")
zzdcl.write( "\tpass\n\n")

zzdcl.close()
INCOMPLETETYPES+=map(lambda x:"declarations."+x,INCOMPLETETYPES)
IGNOREFUNCTIONS+=map(lambda x:"declarations."+x,IGNOREFUNCTIONS)

################################################################################
def decld(n):
  return "declarations."+n
################################################################################


#cythonfile1.write(file("header.py").read().replace("    ","\t"))

#
# generation of wrapper class for instances
#

classes_f=new_cython_file("zopencv_classes.pyx")
classes_d=new_cython_decl_file("zopencv_classes.pxd")
classes_f.write("import zopencv_lowlevel\n")
classes_f.write("import zopencv_pclasses\n")
classes_f.write("import zopencv_classes\n")
classes_f.write("import zopencv_core\n")
classes_f.write("cimport stdlib\n")
classes_f.write("cimport zopencv_lowlevel\n")
classes_f.write("cimport zopencv_pclasses\n")
classes_f.write("cimport zopencv_classes\n")
sys.stderr.write(("#generating classes\n"))
for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Structure) and (not (f.name in INCOMPLETETYPES))):
            if (f.name[0]=="_"):
                sys.stderr.write("forgetting structure beginning with underscore ("+f.name+")...\n")
                continue
            if (not(len(f.members))):
                sys.stderr.write("forgetting empty sructure ("+f.name+")...\n")
                continue
            try:
                f.name.index("DOT")
                sys.stderr.write("forgetting anonymous sructure ("+f.name+")...\n")
                continue
            except:
                pass
            try:
                f.name.index("DOLLAR")
                sys.stderr.write("forgetting anonymous sructure ("+f.name+")...\n")
                continue
            except:
                pass
            classes_f.write( "cdef class "+classname_transform(f.name)+":\n")
            classes_d.write( "cdef class "+classname_transform(f.name)+":\n")
            #print "\t#"+str(f.__dict__)
            classes_f.write( "\t#cdef "+decld(realtype_of(f).name)+ " instance\n")
	    classes_d.write( "\tcdef "+decld(realtype_of(f).name)+ " instance\n")
            classes_f.write( "\tdef __init__(object self, ptr=None):"+"\n")
            classes_d.write( "\t#def __init__(object self, ptr)"+"\n")
            classes_f.write( "\t\tif (ptr):"+"\n")
            classes_f.write( "\t\t\tself.init_from_raw_pointer(ptr)"+"\n")
            classes_f.write( "\tdef init_from_raw_pointer(object self,"+POINTERTYPE+" value):"+"\n")
            classes_f.write( "\t\tself.instance=(<"+ decld(realtype_of(f).name) +" *>value)[0]"+"\n")
            classes_f.write( "\t@staticmethod"+"\n")
            classes_f.write( "\tdef get_sizeof(self):"+"\n")
            classes_f.write( "\t\treturn cython.sizeof("+decld(realtype_of(f).name)+")"+"\n")
	    classes_d.write( "\t#def get_pointer(self)"+"\n")
            classes_f.write( "\tdef get_pointer(self):"+"\n")
            classes_f.write( "\t\treturn <"+POINTERTYPE+">&self.instance"+"\n")
            write_struct_union_members_accessors(f.members,outfile=classes_f)
            export_methods(classes_f,f)
	    classes_d.write( "\tpass"+"\n")

for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Structure) and ((f.name in EXPLICITTYPES))):
            if (f.name[0]=="_"):
                sys.stderr.write("forgetting structure beginning with underscore ("+f.name+")...\n")
                continue
            if (not(len(f.members))):
                sys.stderr.write("forgetting empty sructure ("+f.name+")...\n")
                continue
            try:
                f.name.index("DOT")
                sys.stderr.write("forgetting anonymous sructure ("+f.name+")...\n")
                continue
            except:
                pass
            try:
                f.name.index("DOLLAR")
                sys.stderr.write("forgetting anonymous sructure ("+f.name+")...\n")
                continue
            except:
                pass
            classes_f.write( "cdef class "+classname_transform(f.name)+":\n")
            classes_d.write( "cdef class "+classname_transform(f.name)+":\n")
            #print "\t#"+str(f.__dict__)
            classes_f.write( "\t#cdef "+decld(realtype_of(f).name)+ " instance\n")
	    classes_d.write( "\tcdef "+decld(realtype_of(f).name)+ " instance\n")
            classes_f.write( "\tdef __init__(object self, ptr=None):"+"\n")
            classes_d.write( "\t#def __init__(object self, ptr)"+"\n")
            classes_f.write( "\t\tif (ptr):"+"\n")
            classes_f.write( "\t\t\tself.init_from_raw_pointer(ptr)"+"\n")
            classes_f.write( "\tdef init_from_raw_pointer(object self,"+POINTERTYPE+" value):"+"\n")
            classes_f.write( "\t\tself.instance=(<"+ decld(realtype_of(f).name) +" *>value)[0]"+"\n")
            classes_f.write( "\t@staticmethod"+"\n")
            classes_f.write( "\tdef get_sizeof(self):"+"\n")
            classes_f.write( "\t\treturn cython.sizeof("+decld(realtype_of(f).name)+")"+"\n")
	    classes_d.write( "\t#def get_pointer(self)"+"\n")
            classes_f.write( "\tdef get_pointer(self):"+"\n")
            classes_f.write( "\t\treturn <"+POINTERTYPE+">&self.instance"+"\n")
            write_struct_union_members_accessors(f.members,outfile=classes_f)
            export_methods(classes_f,f)
	    classes_d.write( "\tpass"+"\n")


#
# generation of wrapper class for pointers on instances
#
pointerclasses_f=new_cython_file("zopencv_pclasses.pyx")
pointerclasses_d=new_cython_decl_file("zopencv_pclasses.pxd")
pointerclasses_f.write("import zopencv_classes\n")
pointerclasses_f.write("import zopencv_pclasses\n")
pointerclasses_f.write("import zopencv_lowlevel\n")
pointerclasses_f.write("import zopencv_core\n")
pointerclasses_f.write("cimport stdlib\n")
pointerclasses_f.write("cimport zopencv_classes\n")
pointerclasses_f.write("cimport zopencv_pclasses\n")
pointerclasses_f.write("cimport zopencv_lowlevel\n")
sys.stderr.write(("#generating pointer classes\n"))
for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Structure) and (not (f.name in INCOMPLETETYPES))):
#       if (f.name[0]=="_"):
#         sys.stderr.write("forgetting structure beginning with underscore ("+f.name+")...\n")
#          continue
            if (not(len(f.members))):
                pointerclasses_f.write( "cdef class "+pointerclassname_transform(f.name)+":"+"\n")
		pointerclasses_d.write( "cdef class "+pointerclassname_transform(f.name)+":"+"\n")
                pointerclasses_f.write( "\t#cdef "+decld(realtype_of(f).name)+ "* instance"+"\n")
		pointerclasses_d.write( "\tcdef "+decld(realtype_of(f).name)+ "* instance"+"\n")
                pointerclasses_f.write( "\tdef __init__(object self, "+POINTERTYPE+" ptr):"+"\n")
                pointerclasses_f.write( "\t\t\tself.instance=<"+decld(realtype_of(f).name)+"*>ptr"+"\n")
                pointerclasses_f.write( "\tdef init_from_raw_pointer(object self,"+POINTERTYPE+" value):"+"\n")
                pointerclasses_f.write( "\t\tself.instance[0]=(<"+ decld(realtype_of(f).name) +" *>value)[0]"+"\n")
                pointerclasses_f.write( "\tdef get_pointer(self):"+"\n")
                pointerclasses_f.write( "\t\treturn <"+POINTERTYPE+">self.instance"+"\n")
                pointerclasses_f.write( "\tdef get_pointer_on_pointer(self):"+"\n")
                pointerclasses_f.write( "\t\treturn <"+POINTERTYPE+">&self.instance"+"\n")                
#                cythonfile1.write( "\t\treturn <"+decld(realtype_of(f).name)+">self.instance"+"\n")
                pointerclasses_f.write( "\t@staticmethod"+"\n")
                pointerclasses_f.write( "\tdef get_sizeof(self):"+"\n")
                pointerclasses_f.write( "\t\treturn cython.sizeof("+decld(realtype_of(f).name)+")"+"\n")
                pointerclasses_f.write( "\tdef free(self):"+"\n")
                pointerclasses_f.write( "\t\tfree(<void *>self.instance)"+"\n")
                continue
            try:
                f.name.index("DOT")
                sys.stderr.write("forgetting anonymous sructure ("+f.name+")...\n")
                continue
            except:
                pass
            try:
                f.name.index("DOLLAR")
                sys.stderr.write("forgetting anonymous sructure ("+f.name+")...\n")
                continue
            except:
                pass
            declaredstructlist.append(f.name)
            pointerclasses_f.write( "cdef class "+pointerclassname_transform(f.name)+":"+"\n")
            pointerclasses_f.write( "\tcdef "+decld(realtype_of(f).name)+ "* instance"+"\n")
            pointerclasses_f.write( "\tdef __init__(object self, "+POINTERTYPE+" ptr):"+"\n")
            pointerclasses_f.write( "\t\t\tself.instance=<"+decld(realtype_of(f).name)+"*>ptr"+"\n")
            pointerclasses_f.write( "\tdef init_from_raw_pointer(object self,"+POINTERTYPE+" value):"+"\n")
            pointerclasses_f.write( "\t\tself.instance[0]=(<"+decld(realtype_of(f).name) +" *>value)[0]"+"\n")
            pointerclasses_f.write( "\tdef get_pointer(self):"+"\n")
            pointerclasses_f.write( "\t\treturn <"+POINTERTYPE+">self.instance"+"\n")
            pointerclasses_f.write( "\tdef get_pointer_on_pointer(self):"+"\n")
            pointerclasses_f.write( "\t\treturn <"+POINTERTYPE+">&self.instance"+"\n")                            
            pointerclasses_f.write( "\t@staticmethod"+"\n")
            pointerclasses_f.write( "\tdef get_sizeof(self):"+"\n")
            pointerclasses_f.write( "\t\treturn cython.sizeof("+decld(realtype_of(f).name)+")"+"\n")
            pointerclasses_f.write( "\tdef free(self):"+"\n")
            pointerclasses_f.write( "\t\tfree(<void *>self.instance)"+"\n")
            write_struct_union_members_accessors(f.members,outfile=pointerclasses_f)
            export_methods(pointerclasses_f,f)


#print ""
#print "class "+MODULENAME+":"

#
# basics of enum values
#
for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if (type(f)==typedesc.EnumValue):
            cythonfile1.write( "\t_"+f.name+"="+f.name+"\n")
        if (type(f)==typedesc.Typedef):
            pass


##
## low level functions
##
lowlevel_functions_f=new_cython_file("zopencv_lowlevel.pyx")
lowlevel_functions_d=new_cython_decl_file("zopencv_lowlevel.pxd")
lowlevel_functions_f.write("import zopencv_classes\n")
lowlevel_functions_f.write("import zopencv_pclasses\n")
lowlevel_functions_f.write("import zopencv_core\n")
lowlevel_functions_f.write("cimport stdlib\n")
lowlevel_functions_f.write("cimport zopencv_classes\n")
lowlevel_functions_f.write("cimport zopencv_pclasses\n")
sys.stderr.write(("#generating low-level function wrappers\n"))
for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Function) and (not (f.name in IGNOREFUNCTIONS))):
            #print "\tdef _raw_"+f.name+'(' + ','.join(map(lambda x:"arg_"+x,f.iterArgNames())) + '):'
            #print "\t\t__global__ "+f.name
            lowlevel_functions_f.write( "cdef _raw_"+f.name+'(' + ','.join(map(lambda x: (rawctypestr(x[0]) + " arg_"+x[1]),zip(f.iterArgTypes(),f.iterArgNames()))) + '):\n')
	    lowlevel_functions_d.write( "cdef _raw_"+f.name+'(' + ','.join(map(lambda x: (rawctypestr(x[0]) + " arg_"+x[1]),zip(f.iterArgTypes(),f.iterArgNames()))) + ')\n')
            #sys.stderr.write("forgetting structure beginning with underscore (in "+f.name+")...\n")
            ft=realtype_of(f.returns)
            if (type(ft)==typedesc.Structure):
                lowlevel_functions_f.write( "\tcdef "+decld(ft.name)+" tstor\n")
                lowlevel_functions_f.write( "\tcdef "+POINTERTYPE+" tptr\n")
                lowlevel_functions_f.write( "\ttstor="+decld(f.name)+'(' + ','.join(map(lambda x:argprintstr(x[0],"arg_"+x[1]),zip(f.iterArgTypes(),f.iterArgNames()))) + ')\n')
                lowlevel_functions_f.write( "\ttptr=<"+POINTERTYPE+">&tstor\n")
                lowlevel_functions_f.write( "\treturn zopencv_classes."+classname_transform(ft.name)+"(ptr=tptr)\n")
            elif (type(ft)==typedesc.PointerType) and (type(realtype_of(ft.typ))==typedesc.Structure) and (realtype_of(ft.typ).name in declaredstructlist):
                lowlevel_functions_f.write( "\tcdef "+POINTERTYPE+" tptr\n")
                lowlevel_functions_f.write( "\ttptr=<"+POINTERTYPE+">"+decld(f.name)+'(' + ','.join(map(lambda x:argprintstr(x[0],"arg_"+x[1]),zip(f.iterArgTypes(),f.iterArgNames()))) + ')\n')
                lowlevel_functions_f.write( "\treturn zopencv_pclasses."+pointerclassname_transform(realtype_of(ft.typ).name)+"(ptr=tptr)\n")
            else:
                lowlevel_functions_f.write( (((type(ft)!=typedesc.FundamentalType) or (ft.name!="void") ) and "\treturn " or "\t")+ irawctypestr(ft)+decld(f.name)+'(' + ','.join(map(lambda x:argprintstr(x[0],"arg_"+x[1]),zip(f.iterArgTypes(),f.iterArgNames()))) + ')\n')
            cythonfile1.write( "\t\n")



##
## high level functions
##
highlevel_functions_f=new_cython_file("zopencv_highlevel.pyx")
highlevel_functions_d=new_cython_decl_file("zopencv_highlevel.pxd")
highlevel_functions_f.write("import zopencv_lowlevel\n")
highlevel_functions_f.write("import zopencv_classes\n")
highlevel_functions_f.write("import zopencv_pclasses\n")
highlevel_functions_f.write("import zopencv_core\n")
highlevel_functions_f.write("import sys\n")
lowlevel_functions_f.write("cimport stdlib\n")
highlevel_functions_f.write("cimport zopencv_lowlevel\n")
highlevel_functions_f.write("cimport zopencv_classes\n")
highlevel_functions_f.write("cimport zopencv_pclasses\n")
sys.stderr.write("generating highlevel wrappers\n")
for includef in includes:
    for f in filter(lambda x:try_match_location(includef,x),list(xcvsym[0])):
        if ((type(f)==typedesc.Function) and (not (f.name in IGNOREFUNCTIONS))):
            highlevel_functions_f.write(( "def "+f.name+"("+ ','.join(map(lambda x:"arg_"+x,f.iterArgNames())) + "):\n"))
	    highlevel_functions_d.write(( "#def "+f.name+"("+ ','.join(map(lambda x:"arg_"+x,f.iterArgNames())) + ")\n"))
	    for x in zip(f.iterArgTypes(), f.iterArgNames()):
	      highlevel_functions_f.write( "\tcdef "+rawctypestr(x[0]) +" _arg_"+x[1]+"\n")
	    for x in zip(f.iterArgTypes(), f.iterArgNames()):
              if (opencvcython_disable_check):                
	        highlevel_functions_f.write( "\t_arg_"+x[1]+"="+correctargb(x[0],"arg_"+x[1])+"\n")
              else:
                highlevel_functions_f.write( "\ttry:\n")
	        highlevel_functions_f.write( "\t\t_arg_"+x[1]+"="+correctargb(x[0],"arg_"+x[1])+"\n")
                highlevel_functions_f.write( "\texcept:\n")
                highlevel_functions_f.write( "\t\tsys.stderr.write('error on argument -%s-\\n')\n"%(x[1]))
                highlevel_functions_f.write( "\t\traise\n")                
            highlevel_functions_f.write(( "\treturn zopencv_lowlevel._raw_"+f.name+'(' + ','.join(map(lambda x:"_arg_"+x, f.iterArgNames())) + ')\n'))




##### ####################################################################################################################################################################
##### Higher level module (to be deprecated ??? do we need it ??? )
##### ####################################################################################################################################################################

sys.stderr.write("success\n")
