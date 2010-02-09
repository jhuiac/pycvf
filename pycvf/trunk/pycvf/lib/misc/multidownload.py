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
import sys
import pycurl
import os
import time

try:
    import signal
    from signal import SIGPIPE, SIG_IGN
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except:
    pass


class MultiDownloader:
    class SimpleDownloadReader:
        def __init__(self,filename):
            self.resf=file(filename,"wb")
        def body_callback(self, buf):
            self.resf.write(buf)

    def __init__(self,downloadlist,num_conn=100, connecttimeout=30, timeout=300, verbose=False):
        self.num_conn = num_conn
        self.connecttimeout = connecttimeout
        self.timeout = timeout
        self.verbose=verbose
        self.urls= downloadlist
        self.num_urls=len(self.urls)
        self.num_conn = min(self.num_conn, self.num_urls)
        assert 1 <= self.num_conn <= 10000, "invalid number of concurrent connections"
        if (self.verbose):
           print "----- Getting", self.num_urls, "URLs using", self.num_conn, "connections -----"

    def run(self):
        m = pycurl.CurlMulti()
        m.handles = []
        for i in range(self.num_conn):
            c = pycurl.Curl()
            c.fp = None
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CONNECTTIMEOUT, 30)
            c.setopt(pycurl.TIMEOUT, 300)
            c.setopt(pycurl.NOSIGNAL, 1)
            #    c.setopt(pycurl.SHARE, 1)
            m.handles.append(c)
        # Main loop
        urlsit=iter(self.urls)
        freelist = m.handles[:]
        num_processed = 0
        try:
            e=urlsit.next()
        except:
            e=None
        while (num_processed < self.num_urls):
            # If there is an url to process and a free curl object, add to multi stack
            while e and freelist:
                #url, filename = queue.pop(0)
                url=e[0]
                if self.verbose:
                    print "queuing "+url
                c = freelist.pop()
                #c.data=StringIO.StringIO()
                c.m=MultiDownloader.SimpleDownloadReader(e[1])
                c.setopt(pycurl.URL, url.encode('ascii'))
                c.setopt(pycurl.WRITEFUNCTION, c.m.body_callback)
                m.add_handle(c)
                c.url = url
                try:
                   e=urlsit.next()
                except:
                   e=None
            if self.verbose:
                print "going to perform"
            while 1:
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            # Check for curl objects which have terminated, and add them to the freelist
            if self.verbose:
                print
                print "results"
            while 1:
                num_q, ok_list, err_list = m.info_read()
                for c in ok_list:
                    if self.verbose:
                        print "url:"+c.url
                    m.remove_handle(c)
                    if self.verbose:
                        print "Success:",  c.url, c.getinfo(pycurl.EFFECTIVE_URL)
                    freelist.append(c)
                for c, errno, errmsg in err_list:
                    m.remove_handle(c)
                    if self.verbose:
                        print "Failed: ",  c.url, errno, errmsg
                    freelist.append(c)
                num_processed = num_processed + len(ok_list) + len(err_list)
                if num_q == 0:
                    break
            m.select(1.0)
            time.sleep(1)
        # Cleanup
        for c in m.handles:
            if c.fp is not None:
                c.fp.close()
                c.fp = None
            c.close()
        m.close()

