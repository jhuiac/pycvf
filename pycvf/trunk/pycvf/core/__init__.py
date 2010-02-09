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

import os,sys

pycvf_registration_url="http://jfli.nii.ac.jp/pycvf/registration/?"

def simpleurlencode(xs):
    return reduce(lambda b,x:b+(x.isalnum() and x or '%%%02x'%(ord(x),)),xs.strip(),'')

def ck_fullname(x):
    if (len(x)==0):
        raise ValueError,"You must provide a fullname"
    return x

def ck_institution(x):
    if (len(x)==0):
        raise ValueError,"You must provide an institution name"
    return x

def ck_email(x):
    import re
    if (len(x)==0):
        raise ValueError,"You must provide an email address"
    if not re.match(r"([A-Za-z0-9._\-]+)@([A-Z0-9a-z.\-]+)",x):
        raise ValueError, "Your email does not match our e-mail regexp"
    return x

def ck_usage(x):
    try :
        v=int(x)
        if (v<0) or (v>9):
            raise ValueError,"Your choice must be comprised in-between 0 and 9"
        return v
    except:
        raise ValueError,"You should reply this question with an integer number"
    return x

def ck_boolean(x):
    v=x.lower()
    valid_answers=['y','n','yes','no','true','false']
    if not v in valid_answers:
        raise ValueError,"Your answer must be one of the following :"+", ".join(valid_answers)
    return v in ['y','yes','true']
    

def register_pycvf(fullname="", email="", institution="", usage=0,want_info=True,send_ok=False):
   import getpass
   usages="""
      0 - research on computer vision
      1 - sound/signal processing
      2 - physics / simulations
      3 - finance / economy      
      4 - bio-informatics
      5 - linguistics / natural language processing
      6 - pure statistics
      7 - arts, e-arts   
      8 - content management      
      9 - others
   """
   d={ 'fullname':fullname , 'email': email, 'usage': usage,'want_info':want_info, 'institution': institution}
   ds={ 'fullname':'Please enter your fullname ' , 
        'institution':'Please enter the name of the institution that you are working for/with ' , 
       'email': '\nIt would be convenient for us to have your e-mail address. We engage into not disclosing your e-mail address and not sharing it with any other institution.\n\nYour e-mail address',
        'usage': usages+'\nWhat is the usage you plan to do of PyCVF ',
        'want_info':'We may provide you some info on PyCVF on request. Probably, no more than once per year. \n Do you want to receive PyCVF by e-mail ?'}
   dp={'fullname':ck_fullname,
       'email':ck_email,
       'usage':ck_usage,
       'want_info':ck_boolean,
       'institution':ck_institution       
      }
   dk=ds.keys()
   sys.stderr.write("\n")
   for k in dk:
                cont=False
                while (not cont):
                  try:
                    if str(d[k])!="":
                      sys.stderr.write("%s [%s]: "%(ds[k],str(d[k])))
                    else:
                      sys.stderr.write("%s : "%(k,))
                    r=sys.stdin.readline().strip()
                    if (len(r)==0):
                        r=str(d[k])
                    d[k]=dp[k](r)
                    cont=True
                  except ValueError,e:
                    print "Invalid value : ", e
                    pass
                    
   while (not send_ok):
       sys.stderr.write(" (r) register via internet\n")
       sys.stderr.write(" (S) skip_registration\n")
       sys.stderr.write("Type in your choice and validate with enter:\n")
       answ=sys.stdin.readline().strip().lower()
       if answ in [ "r" , "register" ]:
           send_ok=True
       elif  answ in [ "S" , "skip_registration" ]:
           sys.exit(0)
           
       d['platform']=sys.platform
       r='&'.join(map(lambda i:"%s=%s"%(i[0],simpleurlencode(str(i[1]))),d.items()))
   register_url=pycvf_registration_url+r
   print "doing online registration..."
   print register_url   
   try:
       import urllib
       urllib.urlopen(register_url).read()
   except:
     ## let's try to do that with a browser
     for x in [
                ("curl",""),
                ("wget","-nd"),                
                ("firefox",""),                               
                ("galeon","")   
              ]:
        if (os.system("which "+x[0]+" 2>&1 > /dev/null")==0):
          os.system(" ".join([x[0],x[1],register_url])+ "2&>1 >/dev/null")
          break
      
pycvf_license_accept_file=os.path.join(os.environ['HOME'],'.pycvf-accept-licence-and-registration')
try:
    os.stat(pycvf_license_accept_file)
except:
    import datetime
    sys.stderr.write("""
    PYCVF is released under LGPL v.3.
    It means that you are free to use the software as you want.
    
    However for this software to survive, we need your support.
    For providing you better support in further release, and in order to prove interest that our
    software received, we would appreciate if you would accept to register.
   
    
    
    
    Press Enter to continue to License.
    """)
    sys.stdin.readline()
    pdbd = os.path.dirname(globals()["__file__"])
    os.system(os.environ.get('PAGER','more')+ " "+ pdbd+"/../../LICENSE")
    answer=""
    while answer not in ["yes","no"]:
      sys.stderr.write("Do you accept the term of the license ? (yes/no) \n")
      answer=sys.stdin.readline().strip().lower()
      if (answer!='yes'):
        sys.stderr.write("\nWell, you did not accept the licencse.")
        sys.stderr.write("You cannot legally use the software then, also we would be thankful to you to remove the source code from your machine.\n")       
        sys.exit(-1)
    file(pycvf_license_accept_file,"w").write("# PyCVF License has been accepted on %s" %(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))       
    sys.stderr.write("\nThanks for approving the license\n\n")
    sys.stderr.write("We now would like also to thank you for taking a few more seconds to register as a PyCVF user.")
    register_pycvf()
    