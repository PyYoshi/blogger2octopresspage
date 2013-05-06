Blogger2OctopressPage
=====================

### Usage

Create new page:

```bash
$ cd $HOME/src/octopress
$ rake new_page['old blog']
$ ls -l
```

Generate page's html files:

```bash
$ cd $HOME/src
$ git clone git://github.com/PyYoshi/blogger2octopresspage.git
$ cd blogger2octopresspage
$ mkvirtualenv blogger2octopresspage
$ pip install -r requirements.txt
$ python blogger2octopresspage.py blog-dd-mm-yyyy.xml -n "old-blog" -o blogger_posts
$ cp -rf $HOME/src/blogger2octopresspage/blogger_posts/_post/* $HOME/src/octopress/source/old-blog/
```

### Option

Speed up:

```bash
$ pip install -U lxml
```

### Requirements

* Python 2.7+ or 3.x
* pip
* virtualenv
* virtualenvwrapper
* Jinja2