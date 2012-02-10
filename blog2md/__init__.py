#!/usr/bin/env python

import itertools
import os
import re
import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from html2text import html2text
from HTMLParser import HTMLParser
from time import strftime, strptime

def naver(username):
    try:
        os.mkdir(username)
    except OSError:
        print "Directory {0} already exists. Please remove the directory first.".format(username)
        return False

    postnum = re.compile('post_\d*')
    postid = re.compile('post-view*')

    for pagenum in itertools.count(start=1):
        url = 'http://blog.naver.com/PostList.nhn?blogId={0}&currentPage={1}'.format(username, pagenum)

        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)

        posts = soup.findAll(id=postnum)
        for post in posts:
            try:
                h = HTMLParser()
                title = h.unescape(post.span.text).encode('utf-8') #str
            except:
                continue

            date = strptime(post.p.text, "%Y/%m/%d %H:%M")
            filename = "{0}-{1}.md".format(strftime("%Y-%m-%d", date), title).replace('/', '.')

            archive = os.path.join(username, strftime("%Y-%m", date))
            if not os.path.exists(archive):
                os.mkdir(archive)
            if os.path.exists(os.path.join(archive, filename)):
                return True

            # Save images
            postsoup = post(id=postid)[0]
            for img in postsoup('img'):
                try:
                    if 'postfiles' in img['src']:
                        imagefile = urllib2.unquote(os.path.basename(img['src'][:-8]))
                        image = open(os.path.join(archive, imagefile), 'w')
                        image.write(urllib2.urlopen(img['src']).read())
                        image.close()
                        img['src'] = imagefile
                except:
                    pass

            # Save post
            content = unicode(postsoup)
            content = html2text(content)
            f = open(os.path.join(archive, filename), 'w')
            f.write("Title: {0}\n".format(title))
            f.write("Time: {0}\n\n".format(strftime("%H:%M:00", date)))
            f.write(content.encode('utf-8'))
            f.close()
            print filename

def main(service, username):
    try:
        eval(service)(username)
    except NameError:
        print "Platform '{0}' not supported.".format(sys.argv[1])
