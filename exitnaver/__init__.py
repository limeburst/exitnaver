#!/usr/bin/env python

from __future__ import unicode_literals
from __future__ import print_function
import codecs
import itertools
import os
import re
import uuid
from time import strftime

from bs4 import BeautifulSoup
from html2text import html2text
from dateutil.parser import parse
import requests

def make_room(username):
    try:
        os.mkdir(username)
        return True
    except OSError:
        print("Directory {0} already exists. Please remove the directory first.".format(username))
        return False

def download_file(url, filename):
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print("Failed to download {0} ({1} {2})".format(url, r.status_code, r.reason))
        return False

    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return True

def main(username):
    if not make_room(username):
        return False

    postnum = re.compile(r'post_\d')
    postid = re.compile(r'post-view*')

    for pagenum in itertools.count(start=1):
        url = 'http://blog.naver.com/PostList.nhn?blogId={0}&currentPage={1}'.format(username, pagenum)
        try:
            page = requests.get(url)
            page.raise_for_status()
        except requests.HTTPError:
            print("User or blog not found.")
            return False

        soup = BeautifulSoup(page.text)
        posts = soup.findAll(id=postnum)
        for post in posts:
            try:
                title = post.span.text
                title = "".join(x for x in title if x.isalnum() or x.isspace())
                title = title.strip()
            except:
                continue

            date = parse(post.p.text).timetuple()
            filename = u"{0}-{1}.md".format(strftime("%Y-%m-%d", date), title)

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
                        imagefile = str(os.path.basename(img['src'][:-8]))
                        if "%" in imagefile:
                            imagefile = str(uuid.uuid4()) + "." + imagefile.split(".")[-1]
                        if download_file(img['src'], os.path.join(archive, imagefile)):
                            img['src'] = imagefile
                except:
                    pass

            # Save post
            content = postsoup.prettify()
            content = html2text(content)
            with codecs.open(os.path.join(archive, filename), encoding='utf-8-sig', mode='w') as f:
                f.write("Title: {0}\n".format(title))
                f.write("Time: {0}\n\n".format(strftime("%H:%M:00", date)))
                f.write(content)
            print(filename)

    return True
