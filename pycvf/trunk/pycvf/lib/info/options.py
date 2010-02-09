# -*- coding: utf-8 -*-
import sys,getopt

class Default_Program_Metadata:
    name=sys.argv[0].upper()
    version="0.1"
    author="Bertrand Nouvel (bertrand.nouvel@gmail.com)"
    description="This program has no description"
    copyright="Copyright Bertrand NOUVEL - JFLI - CNRS 2009"

program_metadata=Default_Program_Metadata

option_list=[]

class CmdLineOption:
  def __init__(self,short, long, argname, description, code_to_be_runned):
     global option_list
     option_list.append(self)
     self.short=short
     self.long=long
     self.argname=argname
     self.description=description
     self.code_to_be_runned=code_to_be_runned

def do_parse_options(program_metadata_=None,option_list_=None):
    #global option_list
    global program_metadata,option_list
    sl=""
    ll=[]
    for o in option_list:
       if o.argname:
           if o.short:
              sl+=o.short+":"
           if o.long:
              ll+=[o.long+"="]
       else:
           if o.short:
              sl+=o.short
           if o.long:
              ll+=[o.long]
    go=getopt.getopt(sys.argv[1:],sl,ll)
    if program_metadata_!=None:
       program_metadata=program_metadata_
    if option_list_!=None:
       option_list=option_list_
    for co in go[0]:                                
       if (len(co)):        
          for o in option_list:
             if (o.long and (co[0]=='--'+o.long)) or(o.short and (co[0]=='-'+o.short)) :
                if (o.argname):
                   o.code_to_be_runned(co[1])
                else:
                   o.code_to_be_runned()
    return go[1]

class CmdLineString(CmdLineOption):
   def modify_stringo(self,x):
       self.value=x
   def __init__(self,short, long, argname, description, default):
       self.value=default
       CmdLineOption.__init__(self,short, long, argname, description,self.modify_stringo)


def print_help_and_exit(retcode=0):
        #global program_metadata
        #global option_list
        sys.stderr.write("""#######################################################################################\n""")
        sys.stderr.write(program_metadata.name +"\n")
        sys.stderr.write("version :"+program_metadata.version +"\n")
        sys.stderr.write("author :"+program_metadata.author +"\n")
        sys.stderr.write(program_metadata.copyright +"\n")
        sys.stderr.write("""#######################################################################################\n""")
        for o in option_list:
           sys.stderr.write( "\t%s %s\t\t:%s\t%s\n" % 
                            (  (o.short) and ( (o.long) and  ("-%s/--%s"%(o.short,o.long)) or  ("-%s"%(o.short,) ) ) or  ("--%s"%(o.long,) ) , 
                            o.argname or "", 
                            o.description ,
                            (("default:"+str(o.value)) if hasattr(o,"value") else "" )
                            )     
                          )  
        sys.stderr.write("""#######################################################################################\n""")
        sys.exit(retcode)

help_option=CmdLineOption('h','help',None,'Displays this help message and exit',print_help_and_exit)
