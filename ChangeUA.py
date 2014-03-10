#!/usr/bin/env python

## Script to change the user-agent
# Much of this is from:
# http://www.diveintopython.net/http_web_services/user_agent.html
# and
# http://wolfprojects.altervista.org/changeua.php

import urllib
import urllib2
from urllib import FancyURLopener


class MyOpener(FancyURLopener):

    def __init__(self):
        self.version = 'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0'
        urllib.FancyURLopener.__init__(self)

    def grab_it(self, url, outpath):
        successful = True
        try:
            urlretrieve = MyOpener().retrieve
            urlretrieve(url, outpath)
            return successful
        except Exception:
            successful = False
            return successful


class MyReader(object):

    def read_it(self, url):
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0')
            opener = urllib2.build_opener()
            data = opener.open(request).read()
            return data
        except Exception:
            pass
