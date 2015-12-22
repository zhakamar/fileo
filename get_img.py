#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import os


def download_img(p_url):
    filename = re.search('([^\/]+)$', p_url).group(0)

    if not os.path.exists('img/%s' % filename):
        r = requests.get('http://www.fileo-inter.ru' + p_url)

        if r.status_code == 200:
            with open("img/%s" % filename, 'wb') as fd:
                fd.write(r.content)
