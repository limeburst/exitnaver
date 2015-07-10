#!/usr/bin/env python

import itertools
import os
import re
import urllib2

from BeautifulSoup import BeautifulSoup
from html2text import html2text
from HTMLParser import HTMLParser
from time import strftime
from dateutil.parser import parse


def make_room(username):
    try:
        os.mkdir(username)
        return True
    except OSError:
        print "Directory {0} already exists. Please remove the directory first.".format(username)
        return False


def main(username):
    if not make_room(username):
        return False

    postnum = re.compile('post_\d*')
    postid = re.compile('post-view*')

    for pagenum in itertools.count(start=1):
        url = 'http://blog.naver.com/PostList.nhn?blogId={0}&currentPage={1}'.format(username, pagenum)
        try:
            page = urllib2.urlopen(url)
        except urllib2.HTTPError:
            print "User or blog not found."
            return False

        soup = BeautifulSoup(page)
        posts = soup.findAll(id=postnum)
        for post in posts:
            try:
                h = HTMLParser()
                title = h.unescape(post.span.text).encode('utf-8')
            except:
                continue

            date = parse(post.p.text).timetuple()
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
                        with open(os.path.join(archive, imagefile), 'w') as image:
                            image.write(urllib2.urlopen(img['src']).read())
                        img['src'] = imagefile
                except:
                    pass

            # Save post
            content = unicode(postsoup).replace("&nbsp;", "")
            content = html2text(content)
            with open(os.path.join(archive, filename), 'w') as f:
                f.write("Title: {0}\n".format(title))
                f.write("Time: {0}\n\n".format(strftime("%H:%M:00", date)))
                f.write(content.encode('utf-8'))
            print filename

    return True
