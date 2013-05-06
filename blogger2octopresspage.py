#!/usr/bin/env python
# -*- coding:utf8 -*-
__author__ = 'PyYoshi'

from optparse import OptionParser
import os
import sys
import datetime

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from lxml import etree
except ImportError:
    import xml.etree.cElementTree as etree

import jinja2

def isoparse(s):
    try:
        return datetime.datetime(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]), int(s[14:16]), int(s[17:19]))
    except:
        return None

def parse(markup):
    el = etree.fromstring(markup)
    entries = []
    drafts = []
    blog_title = el.find('{http://www.w3.org/2005/Atom}title').text
    for entry in el.findall('{http://www.w3.org/2005/Atom}entry'):
        category_type = None
        categories = []
        for category in entry.findall('{http://www.w3.org/2005/Atom}category'):
            category_tmp = category.get('term')
            category_tmp_type = category_tmp.split('#')
            if len(category_tmp_type) == 2:
                category_type = category_tmp_type[1]
            else:
                categories.append(category.get('term'))
        if category_type == 'post':
            published = entry.find('{http://www.w3.org/2005/Atom}published')
            title = entry.find('{http://www.w3.org/2005/Atom}title')
            content = entry.find('{http://www.w3.org/2005/Atom}content')
            link = entry.find('{http://www.w3.org/2005/Atom}link[@rel="alternate"]')
            url = None
            if link != None: url = link.get('href')
            permalink = None
            if url != None: permalink = urlparse(url).path
            uuid = entry.find('{http://www.w3.org/2005/Atom}id').text.split('-')[-1]
            d = isoparse(published.text)
            entry_obj = {
                'title' : title.text,
                'published' : d,
                'content': content.text,
                'url' : url,
                'uuid' : uuid,
                'categories' : categories,
                'permalink' : permalink
            }
            if url:
                entries.append(entry_obj)
            else:
                drafts.append(entry_obj)
    return blog_title, entries, drafts

def save_file(text, path, encode='utf8'):
    with open(path, 'wb') as f: f.write(text.encode(encode))

def gen_pages(page_name, entries, drafts, output_dir):
    post_dir = os.path.join(output_dir, '_post')
    draft_dir = os.path.join(output_dir, '_draft')
    if not os.path.exists(post_dir): os.makedirs(post_dir)
    if not os.path.exists(draft_dir): os.makedirs(draft_dir)
    with open('templates/page/entry.html', 'r') as f: template_entry_html = f.read()
    for entry in entries:
        html = jinja2.Environment().from_string(template_entry_html).render(entry)
        filename = entry['published'].strftime('%Y-%m-%d-%H-%M-%S') + '_' + entry['permalink'].split('/')[-1]
        save_file(html,os.path.join(post_dir, filename))
    with open('templates/page/index.markdown', 'r') as f: template_index_markdown = f.read()
    now = datetime.datetime.now()
    markdown = jinja2.Environment().from_string(template_index_markdown).render(page_name=page_name, entries=entries, date=now.strftime('%Y-%m-%d %H:%M'))
    save_file(markdown, os.path.join(post_dir, 'index.markdown'))
    for entry in drafts:
        html = jinja2.Environment().from_string(template_entry_html).render(entry)
        filename = entry['published'].strftime('%Y-%m-%d-%H-%M-%S') + '_draft_post.html'
        save_file(html,os.path.join(draft_dir, filename))

def main():
    parser = OptionParser(usage="Usage: python %s <Blogger's xml path>" % os.path.basename(__file__))
    parser.add_option('-o', '--output_dir', dest='output', type='string', default='blogger_posts')
    parser.add_option('-n', '--page_name', dest='page_name', type='string', default='oldblog', help='Page directory name. e.g) rake new_page["old blog"] page_name="old-blog"')
    options, args = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit()
    if not os.path.exists(args[0]):
        parser.print_help()
        raise Exception('%s can not be found.' % args[0])
    with open(args[0], 'rb') as f: markup = f.read()
    blog_title, entries, drafts = parse(markup)
    gen_pages(options.page_name, entries, drafts, options.output)

if __name__ == '__main__':
    main()
    sys.exit()