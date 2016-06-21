#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
HTMLParser

'''




import sys
import re
import chardet
import urllib
from HTMLParser import HTMLParser

#获取<a>连接和文字

class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.tmp_link = {}
        self.cp_data = False

    def handle_starttag(self, tag, attrs):
            if tag == "a":
                if len(attrs) == 0: pass
                else:
                    for (k,v) in attrs:
                        if k == "href":
                            self.tmp_link['href'] = v
                            self.cp_data = True

    def handle_endtag(self, tag):
            self.cp_data = False

    def handle_data(self, data):
            if self.cp_data:
                self.tmp_link['data'] = data
                self.links.append(self.tmp_link)

    def getResults(self):
            return self.links


def load_targets():
    print 'load targets'

    targets = []
    with open('targets', 'r') as fp:
        ll = fp.readlines()
        for l in ll:
            ww = l.split(',')
            ru={}
            ru['name'] = ww[0].strip()
            ru['url'] = ww[1].strip()
            targets.append(ru)
    
    print 'target count %d'%(len(targets))

    return targets



def compare_info(target):
    infos = []
    name = target['name']
    url = target['url']
    page = urllib.urlopen(url)
    text = page.read()
    page.close()
    print name, url, "%d" %(len(text))

    psr = MyParser()
    psr.feed(text)
    links = psr.getResults()
    psr.close()
    print links

    

    return infos



def notify_info(info):
    pass

def main():
    targets = load_targets()

    for target in targets:
        infos = compare_info(target)
        for info in infos:
            notify_info(info)
    

    




if __name__ == "__main__":

    main()