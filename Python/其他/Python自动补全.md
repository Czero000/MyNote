## Python 自动补全
下面是如何实现PythonTab补全和历史命令管理方法。

### Python的startup文件
为readline添加tab键自动补全功能，像shell一样管理历史命令

- 获取python安装目录

```python
>>> import sys
>>> sys.path
['', '/usr/lib64/python27.zip', '/usr/lib64/python2.7', '/usr/lib64/python2.7/plat-linux2', '/usr/lib64/python2.7/lib-tk', '/usr/lib64/python2.7/lib-old', '/usr/lib64/python2.7/lib-dynload', '/usr/lib64/python2.7/site-packages', '/usr/lib64/python2.7/site-packages/gtk-2.0', '/usr/lib/python2.7/site-packages']
```
安装目录为'/usr/lib64/python2.7'

- 切换目录编写`startup.py`脚本,`cp startup.py /usr/lib64/python2.7/`

```python
#!/usr/bin/env python
# python startup file
import sys
import readline
import rlcompleter
import atexit
import os
# tab completion
readline.parse_and_bind('tab: complete')
# history file
histfile = os.path.join(os.environ['HOME'], '.pythonhistory')
try:
    readline.read_history_file(histfile)
except IOError:
    pass
atexit.register(readline.write_history_file, histfile)
del os, histfile, readline, rlcompleter
```

- 增加环境变量

```shell
edit .bashrc
// 增加下面内容
export PYTHONSTARTUP=/usr/lib64/python2.7/startup.py

// 变量生效
source .bashrc
```

### vim增加自动补全

- 下载插件

[pydiction](http://www.vim.org/scripts/script.php?script_id=850):http://www.vim.org/scripts/script.php?script_id=850

- 安装插件

```
wget http://www.vim.org/scripts/download_script.php?src_id=21842
unzip pydiction-1.2.3.zip
cp pydiction/after/ftplugin/python_pydiction.vim /usr/share/vim/vim74/ftplugin/
mkdir /usr/share/vim/vim74/pydiction
cp pydiction/complete-dict /usr/share/vim/vim74/pydiction/
cp pydiction/pydiction.py  /usr/share/vim/vim74/pydiction/
```
- 修改vim配置文件

```
let g:pydiction_location = '/usr/share/vim/vim74/pydiction/complete-dict'
let g:pydiction_menu_height = 20
```
