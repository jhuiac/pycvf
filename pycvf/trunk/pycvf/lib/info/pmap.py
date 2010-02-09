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


#!/usr/bin/env python
# -*- coding: utf-8 -*-


##
## Copyright of orignial file :

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials
#       provided with the distribution.
#
#     * Neither the name of Kirk Strauser nor the names of its
#       contributors may be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Very basic parallel processing support

Replaces the built-in map() function with a version that can run
across many processes simultaneously.  Attempts to replicate the
semantics of map() as precisely as possible so that it can be used in
all situations with little surprise.
"""

__author__  = "Kirk Strauser <kirk@strauser.com>"
__version__ = "$Rev: 1139 $"
__date__    = "$Date: 2007-05-24 10:56:44 -0500 (Thu, 24 May 2007) $"

import cPickle
import os
import signal
import struct
import sys
import itertools
import select
import __builtin__

from pycvf.core.errors import *

def myzip(*sequences):
  class MZipIterator:
      def __len__(self):
          return max(map(len,sequences))
      def __iter__(self):
          iters=map(iter,sequences)
          for x in range(len(self)):
              yield map(lambda i:i.next(),iters)
      def __getitem__(self,n):
          return map(lambda i:i[n],sequences)
  return MZipIterator()

def map(function, *sequence):
    """map(function, sequence[, sequence, ...]) -> list

    Like the builtin map() function, but splits the workload across a
    pool of processes whenever possible.

    >>> map(None, [1,2,3])
    [1, 2, 3]
    >>> map(None, [1,2,3], [5,6])
    [(1, 5), (2, 6), (3, None)]
    """

    # IPC stuff
    structformat = 'I'
    structlen = struct.calcsize(structformat)

    def sendmessage(myend, message):
        """Send a pickled message across a pipe"""
        outobj = cPickle.dumps(message)
        os.write(myend, struct.pack(structformat, len(outobj)) + outobj)

    def recvmessage(myend):
        """Receive a pickled message from a pipe"""
        try:
           length = struct.unpack(structformat, (os.read(myend, structlen)))[0]
           return cPickle.loads(os.read(myend, length))
        except ValueError:
           pycvf_warning("PMAP : pickle failed to decode message / Communication Error ???")
           return None
           

    try:
        maxchildren = function.parallel_maxchildren
    except AttributeError:
        return __builtin__.map(function, *sequence)

    # Handle map()'s multi-sequence semantics
    if len(sequence) == 1:
        if function is None:
            return list(sequence[0])
#        arglist = zip(sequence[0])
        arglist = myzip(sequence[0])
    else:
#        arglist = __builtin__.map(None, *sequence)
        arglist = myzip(*sequence)
    len_arglist=(max(map(len,sequence)))
    if function is None:
        return arglist

    argindex = 0
    finished = 0
    outlist = [None] * len_arglist

    # Spawn the worker children.  Don't create more than the number of
    # values we'll be processing.
    #fromchild, toparent = os.pipe()
    pipes = [ os.pipe() for i  in min(maxchildren, len(arglist)) ]  
    children = []
    for childnum in range(min(maxchildren, len(arglist))):
        fromparent, tochild = pipes[childnum]
        pid = os.fork()
        # Parent?
        if pid:
            # Do some housekeeping and give the child its first assignment
            children.append({'pid'       : pid,
                             'fromparent': fromparent,
                             'tochild'   : tochild
                             })
            sendmessage(tochild, (argindex, arglist[argindex]))
            argindex += 1
        # Child?
        else:
            # Since children can't really tell when they've been
            # orphaned, set a timeout so that they die if they don't
            # hear from the parent in a timely manner.
            def timeouthandler(signum, frame):
                """Get out cleanly"""
                sys.exit()
            oldsignal = signal.signal(signal.SIGALRM, timeouthandler)

            # Keep processing values until the parent kills you
            while True:
                try:
                    # Wait one second before quitting.  Children
                    # should generally hear from their parent almost
                    # instantly.
                    signal.alarm(1)
                    message = recvmessage(fromparent)
                    signal.alarm(0)
                    if message is None:
                        sys.exit()
                    index, value = message
                    sendmessage(toparent, (childnum, index, function(*value)))
                except Exception, excvalue:
                    sendmessage(toparent, (childnum, index, excvalue))
                finally:
                    signal.signal(signal.SIGALRM, oldsignal)

    # Keep accepting values back from the children until they've all
    # come back
    while finished < len(arglist):
        returnchild, returnindex, value = recvmessage(fromchild)
        if isinstance(value, Exception):
            raise value
        outlist[returnindex] = value
        finished += 1
        # If there are still values left to process, hand one back out
        # to the child that just finished
        if argindex < len(arglist):
            sendmessage(children[returnchild]['tochild'],
                        (argindex, arglist[argindex]))
            argindex += 1

    # Kill the child processes
    [sendmessage(child['tochild'], None) for child in children]
    [os.wait() for child in children]

    return outlist


def xmap(function, onreturn, *sequence):
    """map(function, sequence[, sequence, ...]) -> list

    Like the builtin map() function, but splits the workload across a
    pool of processes whenever possible.

    >>> map(None, [1,2,3])
    [1, 2, 3]
    >>> map(None, [1,2,3], [5,6])
    [(1, 5), (2, 6), (3, None)]
    """

    # IPC stuff
    structformat = 'I'
    structlen = struct.calcsize(structformat)

    
    def sendmessage_orig(myend, message):
        """Send a pickled message across a pipe"""
        outobj = cPickle.dumps(message)
        os.write(myend, struct.pack(structformat, len(outobj)) + outobj)

    def recvmessage_orig(myend):
        """Receive a pickled message from a pipe"""
        try:
           length = struct.unpack(structformat, (os.read(myend, structlen)))[0]
           return cPickle.loads(os.read(myend, length))
        except ValueError:
           pycvf_warning("PMAP : pickle failed to decode message / Communication Error ???")
           return None
       
    def sendmessage(myend, message):
        """Send a pickled message across a pipe"""
        outobj = cPickle.dumps(message)
        buf=struct.pack(structformat, len(outobj)) + outobj
        length=len(buf)
        while (length>0):
           length-=os.write(myend, buf)

    def recvmessage(myend):
        """Receive a pickled message from a pipe"""
        ilength=0
        try:
           ilength=length = struct.unpack(structformat, (os.read(myend, structlen)))[0]
           buf=""
           while(length>0):
             rd=os.read(myend, length)
             buf+=rd
             length-=len(rd)
           return cPickle.loads(buf)
        except ValueError:
           pycvf_warning("PMAP : pickle failed to decode message / Communication Error ??? (il=%d) "%(ilength,))
           return None
    try:
        maxchildren = function.parallel_maxchildren
    except AttributeError:
        return __builtin__.map(function, *sequence)

    # Handle map()'s multi-sequence semantics
    if len(sequence) == 1:
        if function is None:
            return sequence[0]
        arglist = myzip(sequence[0])
    else:
#        arglist = __builtin__.map(None, *sequence)
        arglist = myzip(*sequence)
    len_arglist=(max(map(len,sequence)))        
    if function is None:
        return arglist

    argindex = 0
    finished = 0

    # Spawn the worker children.  Don't create more than the number of
    # values we'll be processing.
    #fromchild, toparent = os.pipe()
    children = []
    iarglist=iter(arglist)
    pipes = [ os.pipe() for i in range(min(maxchildren, len(arglist))) ]
    for childnum in range(min(maxchildren, len_arglist)):
        fromchild, toparent = pipes[childnum]#os.pipe()        
        fromparent, tochild = os.pipe()
        pid = os.fork()
        # Parent?
        if pid:
            # Do some housekeeping and give the child its first assignment
            children.append({'pid'       : pid,
                             'fromparent': fromparent,
                             'tochild'   : tochild,
                             })
            sendmessage(tochild, (argindex, iarglist.next()))
            argindex += 1
        # Child?
        else:
            # Since children can't really tell when they've been
            # orphaned, set a timeout so that they die if they don't
            # hear from the parent in a timely manner.
            def timeouthandler(signum, frame):
                """Get out cleanly"""
                pycvf_warning("Child process died because of absence of comunication with parent...")                
                sys.exit()
            oldsignal = signal.signal(signal.SIGALRM, timeouthandler)

            # Keep processing values until the parent kills you
            while True:
                try:
                    # Wait one second before quitting.  Children
                    # should generally hear from their parent almost
                    # instantly.
                    signal.alarm(15)
                    message = recvmessage(fromparent)
                    signal.alarm(0)
                    if message is None:
                        sys.exit()
                    index, value = message
                    sendmessage(toparent, (childnum, index, function(*value)))
                except Exception, excvalue:
                    sendmessage(toparent, (childnum, index, excvalue))
                finally:
                    signal.signal(signal.SIGALRM, oldsignal)

    # Keep accepting values back from the children until they've all
    # come back
    fromchildl=map(lambda x:x[0],pipes)
    while finished < len_arglist:
        ready=select.select(fromchildl,[],[])[0]
        fromchild=ready[0]
        res = recvmessage(fromchild)
        if res!=None:
           returnchild, returnindex, value = res
           if isinstance(value, Exception):
             raise value
        onreturn(returnindex, value)
        finished += 1
        # If there are still values left to process, hand one back out
        # to the child that just finished
        if argindex < len_arglist:
            sendmessage(children[returnchild]['tochild'],
                        (argindex, iarglist.next()))
            argindex += 1

    # Kill the child processes
    [sendmessage(child['tochild'], None) for child in children]
    [os.wait() for child in children]



def parallelizable(maxchildren=2, perproc=None):
    """Mark a function as eligible for parallelized execution.  The
    function will run across a number of processes equal to
    maxchildren, perproc times the number of processors installed on
    the system, or the number of times the function needs to be run to
    process all data passed to it - whichever is least."""
    if perproc is not None:
        processors = 4 # hand-waving
        maxchildren = min(maxchildren, perproc * processors)
    def decorate(f):
        """Set the parallel_maxchildren attribute to the value
        appropriate for this function"""
        setattr(f, 'parallel_maxchildren', maxchildren)
        return f
    return decorate

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    @parallelizable(10, perproc=4)
    def timestwo(x, y):
        """Make pylint happy"""
        return (x + y) * 2
    print map(timestwo, [1, 2, 3, 4], [7, 8, 9, 10])

    @parallelizable(10)
    def busybeaver(x):
        """Make pylint happy"""
        for i in range(1000000):
            x = x + i
        return x
    print map(busybeaver, range(27))
