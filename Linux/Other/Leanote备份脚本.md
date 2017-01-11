title: Leanote备份脚本
date: 2017/01/11 12:04:42
updated: 2017/01/11 12:14:00
categories:
- Other
- Leanote
---
为知笔记收费了，把笔记迁移到 leanote 上，但是有担心笔记的安全，所以找到了一个备份脚本，每天备份日志到本地。

- 备份脚本
```python
cat Leanote4MD.py

#!/usr/bin/env python
#encoding: utf8
#
# author: goodbest <lovegoodbest@gmail.com>
# github: github.com/goodbest

import requests
import json
import os
import sys
from datetime import datetime
import dateutil.parser
from dateutil import tz
from PIL import Image
from StringIO import StringIO
from requests_toolbelt import SSLAdapter
import ssl
import argparse
import ConfigParser as CP

leanote_host = None
leanote_token = None
local_zone = None
args = None

configpath = "Leanote.cfg"

DEBUG = 0

def is_ok(myjson):
    try:
      json_object = json.loads(myjson)
    except ValueError, e:
        print e
        return False

    if 'Ok' in json_object:
        if json_object['Ok']:
            return True
        else:
            print json_object['Msg']
            return False
    else:
        return True


def req_get(url, param = '', type = 'json', token = True):
    if token:
        if param:
            param.update({'token': leanote_token})
        else:
            param={'token': leanote_token}

    s = requests.Session()
    if leanote_host.startswith('https'):
        s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))
    r = s.get(leanote_host + '/api/' + url, params = param)
    if r.status_code == requests.codes.ok:
        if type=='json':
            if is_ok(r.text):
                rj = json.loads(r.text)
                # if 'Msg' in rj:
                #     rj=rj['Msg']
                return rj
            else:
                print '[Err] requests to url %s fail' %(r.url)
                return None
        elif type=='image':
            i = Image.open(StringIO(r.content))
            return i

    else:
        print '[Err] connect to url %s fail, error code %d ' %(r.url, r.status_cde)
        return None


def req_post(url, param = '', type = 'json', token = True):
    if token:
        if param:
            param.update({'token': leanote_token})
        else:
            param={'token': leanote_token}

    s = requests.Session()
    if leanote_host.startswith('https'):
        s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))
    r = s.post(leanote_host + '/api/' + url, data = param)
    if r.status_code == requests.codes.ok:
        if type=='json':
            if is_ok(r.text):
                rj = json.loads(r.text)
                # if 'Msg' in rj:
                #     rj=rj['Msg']
                return rj
            else:
                print '[Err] requests to url %s fail' %(r.url)
                return None

    else:
        print '[Err] connect to url %s fail, error code %d ' %(r.url, r.status_cde)
        return None


#ret leanote_token
def login(email, pwd):
    param = {
        'email': email,
        'pwd':   pwd,
    }
    r = req_get('auth/login', param, token=False)
    if r:
        print 'Login success! Welcome %s (%s)' %(r['Username'], r['Email'])
        return r['Token']
    else:
        print 'Login fail! Start again.'
        exit()


def logout():
    return req_get('auth/logout')


#ret dict(notebookId: type.Notebook}
def getNotebooks(includeTrash = False):
    r = req_get('notebook/getNotebooks')
    if r:
        if includeTrash:
            return {notebook['NotebookId'] : notebook for notebook in r}
        else:
            return {notebook['NotebookId'] : notebook for notebook in r if not notebook['IsDeleted']}
    else:
        return


#ret [type.Note], which contains noteId, and note meta data
def getNotesMeta(notebookId):
    param = {
        'notebookId': notebookId,
    }
    return req_get('note/getNotes', param)


#ret type.NoteContent
def getNoteDetail(noteId):
    param = {
        'noteId': noteId,
    }
    return req_get('note/getNoteAndContent', param)


def getImage(fileId):
    param = {
        'fileId': fileId,
    }
    return req_get('file/getImage', param, type = 'image')


def addNotebook(title='Import', parentId='', seq=-1):
    param = {
        'title': title,
        'parentNotebookId': parentId,
        'seq' : seq
    }
    return req_post('notebook/addNotebook', param)


def addNote(NotebookId, Title, Content, Tags=[], IsMarkdown = True, Abstract= '', Files=[]):
    param = {
        'NotebookId': NotebookId,
        'Title': Title,
        'Content': Content,
        'Tags[]': Tags,
        'IsMarkdown': IsMarkdown,
        'Abstract': Abstract,
        #'Files' : seq
    }
    return req_post('note/addNote', param)


def readFromFile(filename):
    import yaml
    file_meta = ''
    file_content = ''
    with open (filename) as f:
        meta_flag=False
        for line in f:
            #print line
            if meta_flag:
                file_content += line
            else:
                if line.find('---')>-1:
                    meta_flag = True
                else:
                    file_meta += line

    if not meta_flag:
        file_content = file_meta
        file_meta = ''

    if meta_flag:
        meta = yaml.load(file_meta)
    else:
        meta = {}
    return file_content, meta


def saveToFile(notes, noteBooks, path = '.'):
    unique_noteTitle = set()
    for note in notes:
        if note['Title'] == '':
            filename = note['NoteId']
        else:
            filename = note['Title']

        if filename in unique_noteTitle:
            filename='%s_%s' %(filename, note['NoteId'])
        else:
            unique_noteTitle.add(filename)

        if note['IsMarkdown']:
            filename += '.md'
        else:
            filename += '.txt'
        try:
            with open(path + '/' + filename, 'w') as file:
                print 'write file: %s' %filename
                file.write('title: %s\n' %note['Title'].encode('utf-8'))


                date = dateutil.parser.parse(note['CreatedTime'])
                file.write('date: %s\n' %datetime.strftime(date.astimezone(local_zone), '%Y/%m/%d %H:%M:%S'))

                date = dateutil.parser.parse(note['UpdatedTime'])
                file.write('updated: %s\n' %datetime.strftime(date.astimezone(local_zone), '%Y/%m/%d %H:%M:%S'))

                if note['Tags']:
                    if len(note['Tags']) == 1:
                        if note['Tags'][0]:
                            file.write('tags:\n')
                            for tag in note['Tags']:
                                file.write('- %s\n' %tag.encode('utf-8'))

                category = []
                current_notebook = note['NotebookId']
                category.append(noteBooks[current_notebook]['Title'])
                while noteBooks[current_notebook]['ParentNotebookId'] != '':
                    category.append(noteBooks[noteBooks[current_notebook]['ParentNotebookId']]['Title'])
                    current_notebook = noteBooks[current_notebook]['ParentNotebookId']
                file.write('categories:\n')
                category.reverse()
                for cat in category:
                    file.write('- %s\n' %cat.encode('utf-8'))

                file.write('---\n')
                file.write('%s' %note['Content'].encode('utf-8'))

            file.close()
            if note['Files']:
                if len(note['Files']) > 0:
                    for attach in note['Files']:
                        if not attach['IsAttach']:
                            i = getImage(attach['FileId'])
                            print 'saving its image: %s.%s' %(attach['FileId'], i.format)
                            i.save(attach['FileId'] + '.' + i.format)

        except:
            print "error: ", filename


def LeanoteExportToMD(path = '.'):
    print 'Reading your notebooks...'
    noteBooks = getNotebooks()

    #get not deleted notes list
    notes=[]
    for notebook in noteBooks.values():
        if not notebook['IsDeleted']:
            notesMeta = getNotesMeta(notebook['NotebookId'])
            for noteMeta in notesMeta:
                    if not noteMeta['IsTrash']:
                        note = getNoteDetail(noteMeta['NoteId'])
                        notes.append(note)
    print 'found %d notes' %len(notes)

    #write file
    saveToFile(notes, noteBooks, path = path)
    print 'all done, bye~'


def LeanoteImportFromMD(path='.'):
    # filelist = os.listdir(path)
    # filelist = [file for file in filelist if file.find('.md')>-1 or file.find('.txt')>-1]

    filelist = readfiles(path)

    importedNotebookTitleMapID = {}
    ret = addNotebook(title='imported_note', parentId='', seq=-1)
    if ret:
        print 'imporing into a new notebook: %s' %ret['Title']
        importedNotebookTitleMapID['import'] = ret['NotebookId']

    for filename in filelist:
        content, meta = readFromFile(path + '/' + filename)
        if DEBUG:
            print meta

        parentTitle='import'
        currentTitle=''
        if meta.get('categories'):
            categories= meta.get('categories')
        else:
            categories=['import']
        for cat in categories:
            currentTitle=cat
            if currentTitle in importedNotebookTitleMapID.keys():
                parentTitle=currentTitle
            else:
                ret = addNotebook(title = currentTitle, parentId = importedNotebookTitleMapID[parentTitle])
                importedNotebookTitleMapID[currentTitle] = ret['NotebookId']
                parentTitle=currentTitle

        if not meta.get('title'):
            meta['title'] = filename.replace('.md','').replace('.txt','')
        importedNote = addNote(NotebookId=importedNotebookTitleMapID[currentTitle], Title=meta.get('title'), Content=content, Tags=meta.get('tags', []), Abstract='')
        if importedNote:
            print 'imported %s' %filename
    print 'all done, bye~'

def readfiles(path):
    assert os.path.exists(path)
    filelist = [os.path.join(root, f) for root,_,files in os.walk(path) for f in files if f.find('.md')>-1 or f.find('.txt')>-1]
    assert filelist, "No files fond in %s" % path
    return filelist


def main():
    global leanote_host
    global leanote_token
    global local_zone
    global args

    args = init_options()

    leanote_host=args.host
    leanote_email=args.user
    leanote_password=args.passwd
    path = args.path

    print 'Connecting to %s' %leanote_host
    leanote_token = login(leanote_email, leanote_password)
    local_zone=tz.tzlocal()

    if args.choice == 'import':
        LeanoteImportFromMD(path)
    elif args.choice == 'export':
        LeanoteExportToMD(path)
    else:
        print 'command format: \npython Leanote4MD.py import\npython Leanote4MD.py export'

    logout()

def init_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("choice", choices=["import", "export"], help="import or export")
    parser.add_argument("--host", dest="host", help="host(defalt:http://leanote.com)")
    parser.add_argument("-u", "--user", dest="user", help="email for login")
    parser.add_argument("-p", "--passwd", dest="passwd",help="passwd for login")
    parser.add_argument("--path", dest="path", help="your save path (default is current dir)")
    args = parser.parse_args()

    config_args = readconfig()
    if not args.host:
        args.host = config_args.get("host")
    if not args.user:
        args.user = config_args.get("email")
    if not args.passwd:
        args.passwd = config_args.get("passwd")
    if not args.path:
        args.path = config_args.get("path")

    if DEBUG:
        print "choice:", args.choice
        print "host:", args.host
        print "user:",args.user
        print "passwd:",args.passwd
        print "path:", args.path

    return args

def readconfig():
    args = {}
    config = CP.ConfigParser()
    config.read(configpath)
    args["host"] = config.get("conn", "host")
    args["email"] = config.get("conn", "email")
    args["passwd"] = config.get("conn", "passwd")
    args["path"] = config.get("conn", "path")
    return args

if __name__ == '__main__':
    sys.exit(main())
```

- 备份脚本说明
```
#leanote导入导出MD工具
- 可以把你储存在[Leanote](http://leanote.com)上的笔记、文章都导出成Markdown文件、文本文件
- 也可以把你储存在硬盘的Markdown文件、文本文件都导入到[Leanote](http://leanote.com)上去
- 目前支持导入导出含YAML格式的meta信息的文件，参照 [hexo](http://hexo.io/docs/front-matter.html)  的文件格式，也就是说文件头部可以有`title` `tags` 
`date` `categoris`等meta信息
- 兼容官方网站，以及自建的服务器（基于beta4，以及API 0.1版本）

#如何使用
- 首先安装Python2版本
- 确保机器已经安装 `requests` `Pillow` `PyYaml` `requests_toolbelt` 等模块，如果没装请 `pip install`
- 然后在命令行执行`python leanote4MD.py`
  - 如果报错，应该是你的 python 路径问题，或者缺少某些python module
- 根据提示输入域名（默认是http://leanote.com）、用户邮箱、密码
  - 域名不要忘记加`http://`
  - 如果是自建服务器，请保证版本不低于 beta4
  - 记得用邮箱，而不是用户名
- 一般导入的错误都是文件没有严格按照YAML格式（多余空格等）造成的解析错误


#功能

- [x] 从Leanote导入、导出笔记本/子笔记本到MD或txt文本文件
- [x] 保存为兼容 hexo front matter 的tag、category、date、title等
  - 由于0.1版本API限制，导入时暂时无法设置 保存时间、修改时间
- [x] 只导入、导出不在垃圾箱的笔记
- [x] 数不尽的bug
- [ ] 根据是否为已发布的blog，生成post或者draft属性
- [x] 导出时保存图片到本地
- [ ] 导入时提交图片到服务器
```

- 备份脚本配置文件，原始备份脚本是交互式的，改为读取配置文件了

```
cat Leanote.cfg
[conn]
host = http://leanote.com
email = charlie.cui@qq.com
passwd = 
path = /opt/Leanote4MD/LeaNote_BackUp/
```

- 备份脚本
```shell
more backupnote 
#!/bin/bash
_work_dir=/opt/Leanote4MD
_date=`date +%Y-%m-%d`

backup() {
	mkdir -p ${_work_dir}/LeaNote_BackUp/${_date}
	cd _${_work_dir}/LeaNote_BackUp
	${_work_dir}/Leanote4MD.py export |tee $LogFile
	mv *.md ${_date}
}

clean(){
	find  ${_work_dir}/LeaNote_BackUp/ -type d -mtime +30 |xargs rm -fr
}
backup && clean 
```

- 增加cron，每天备份一次