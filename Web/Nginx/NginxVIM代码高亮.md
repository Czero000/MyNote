配置Vim 支持Nginx 配置文件高亮显示
* 下载 Nginx 配置文件的 Vim 语法高亮：`http://www.vim.org/scripts/script.php?script_id=1886`
* 将下载的`nginx.vim`复制到`~/.vim/syntax/`文件夹下，并且在`~/.vim/filetype.vim`文件中
* `echo "au BufRead,BufNewFile /usr/local/nginx/* set ft=nginx" >> /root/.vim/filetype.vim`

 ### 配置Vim的Nginx配置文件语法高亮的脚本，写成脚本，免得每次都手动配置。
 ```
 #!/bin/bash
 [[ -d ~/.vim/syntax ]] || mkdir  -p ~/.vim/syntax
 wget http://www.vim.org/scripts/download_script.php?src_id=19394 -O ~/.vim/syntaxnginx.vim/
 echo "au BufRead,BufNewFile /usr/local/nginx/* set ft=nginx" >> ~/.vim/filetype.vim
 ```

 [nginx.vim文件下载链接](https://czero000.github.io/upload/web/nginx/nginx.vim)
