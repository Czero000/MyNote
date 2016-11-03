hexo是一个基于Node.js的静态博客，可以生成静态页面，直接放到国外的GitHub或者是国内的GitCafe等代码托管网站。

## 系统环境准备
系统环境*Windows7 64bit*
文本编辑器：MarkdowanPad2

### 安装Node.JS

到[Node.JS](https://nodejs.org/en/)官方网站下载[最新版本](https://nodejs.org/download/),默认安装即可，我用的是[node-v4.1.1-x64.msi ](https://nodejs.org/download/release/v4.1.1/node-v4.1.1-x64.msi)

### 安装GIT Client

Git的客户端有很多，我使用的是[git](https://git-for-windows.github.io/)

### 安装编辑器

[MarkdownPad](http://markdownpad.com/)是Windows下的一个全功能Markdown编辑器

* 注册信息
````
Mail：Soar360@live.com
Key：GBPduHjWfJU1mZqcPM3BikjYKF6xKhlKIys3i1MU2eJHqWGImDHzWdD6xhMNLGVpbP2M5SN6bnxn2kSE8qHqNY5QaaRxmO3YSMHxlv2EYpjdwLcPwfeTG7kUdnhKE0vVy4RidP6Y2wZ0q74f47fzsZo45JE2hfQBFi2O9Jldjp1mW8HUpTtLA2a5/sQytXJUQl/QKO0jUQY4pa5CCx20sV1ClOTZtAGngSOJtIOFXK599sBr5aIEFyH0K7H4BoNMiiDMnxt1rD8Vb/ikJdhGMMQr0R4B+L3nWU97eaVPTRKfWGDE8/eAgKzpGwrQQoDh+nzX1xoVQ8NAuH+s4UcSeQ==
````

### GitHub
* 注册一个GitHub帐号
* 建立与你用户名对应的仓库，仓库名必须为 **you_user_name.github.io
* 配置SSH，请参考SSH[配置教程](https://help.github.com/articles/generating-ssh-keys/)


### Hexo

安装Hexo
````
//2.x 
npm install hexo -g
//3.x
npm install hexo-cli -g
npm install hexo --save
````

查看hexo版本
```
hexo version
```

创建项目
```
mkdir hexo_dir
hexo init hexo_dir #(hexo_dir为自己定义的目录)
```

安装依赖包
```
//2.x
npm install

// 3.x
npm install
// generators
npm install hexo-generator-index --save
npm install hexo-generator-archive --save
npm install hexo-generator-category --save
npm install hexo-generator-tag --save
// server
npm install hexo-server --save
// deployers
npm install hexo-deployer-git --save
npm install hexo-deployer-heroku --save
npm install hexo-deployer-rsync --save
npm install hexo-deployer-openshift --save
// plugins
npm install hexo-renderer-marked@0.2 --save
npm install hexo-renderer-stylus@0.2 --save
npm install hexo-generator-feed@1 --save
npm install hexo-generator-sitemap@1 --save
```
之后所有的命令都应该在这个目录下面进行

启动服务
```
hexo server
```

现在打开``http://localhost:4000/`` 或者 ``http://127.0.0.1:4000/`` 就可以看到网页了。


## 使用Hexo

### 目录结构
```
.
├── .deploy       #需要部署的文件
├── node_modules  #Hexo插件
├── public        #生成的静态网页文件
├── scaffolds     #模板
├── source        #博客正文和其他源文件, 404 favicon CNAME 等都应该放在这里
|   ├── _drafts   #草稿
|   └── _posts    #文章
├── themes        #主题
├── _config.yml   #全局配置文件
└── package.json
```

### 网站配置文件_config.yml

```
# Hexo Configuration
## Docs: http://hexo.io/docs/configuration.html
## Source: https://github.com/hexojs/hexo/

# Site
title: 点滴分享 多彩生活
subtitle: Free My Mind 
description: 一个技术宅的Blog
author: Charlie.Cui
language: zh-Hans
timezone: Asia/Shanghai
keywords: Hexo,Blog

# URL
## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
url: http://zerocyl.gitcafe.io
root: /
permalink: :year/:month/:day/:title/
#permalink: :categories/:title/
permalink_defaults:
avatar: http://7xlw3d.com1.z0.glb.clouddn.com/zerounix-avatar.jpg

# Directory
source_dir: source
public_dir: public
tag_dir: tags
archive_dir: archives
category_dir: categories
code_dir: downloads/code
i18n_dir: :lang
skip_render:

# Writing
#new_post_name: :lang/:title.md # File name of new posts
default_layout: post
titlecase: false # Transform title into titlecase
external_link: true # Open external links in new tab
filename_case: 0
render_drafts: false
post_asset_folder: false
relative_link: false
future: true
highlight:
  enable: true
  line_number: false
  auto_detect: true
  tab_replace:

# Category & Tag
default_category: uncategorized
category_map:
tag_map:

# Date / Time format
## Hexo uses Moment.js to parse and display date
## You can customize the date format as defined in
## http://momentjs.com/docs/#/displaying/format/
date_format: YYYY-MM-DD
time_format: HH:mm:ss

# Pagination
## Set per_page to 0 to disable pagination
per_page: 10
pagination_dir: page

#归档页数
index_generator:
  per_page: 5

archive_generator:
  per_page: 20
  yearly: true
  monthly: true

tag_generator:
  per_page: 10
  
# Extensions
## Plugins: http://hexo.io/plugins/
plugins:
 - hexo-generator-sitemap
 - hexo-generator-baidu-sitemap
## Themes: http://hexo.io/themes/
theme: next

# Deployment
## Docs: http://hexo.io/docs/deployment.html
deploy:
  type: git
  #repository: git@gitcafe.com:zerocyl/zerocyl.git
  #branch: gitcafe-pages
  repo:
    github: git@github.com:zerocyl/zerocyl.github.io,master
    gitcafe: git@gitcafe.com:zerocyl/zerocyl.git,gitcafe-pages

#百度分析ID  
baidu_analytics: e6a69fa637c84025d15c29301321ff69

#多说域名
duoshuo_shortname: zerocylgit

#建站时间
since: 2015

# Creative Commons 4.0 International License.
# http://creativecommons.org/
# Available: by | by-nc | by-nc-nd | by-nc-sa | by-nd | by-sa | zero
creative_commons: by-nc-sa

#hexo sitemap
sitemap:
path: sitemap.xml

baidusitemap:
path: baidusitemap.xml

```
### 命令行使用介绍
####常用命令

```
hexo help #查看帮助
hexo init #初始化一个目录
hexo new "postName" #新建文章
hexo new page "pageName" #新建页面
hexo generate #生成网页, 可以在 public 目录查看整个网站的文件
hexo server #本地预览, 'Ctrl+C'关闭
hexo deploy #部署.deploy目录
hexo clean #清除缓存, **强烈建议每次执行命令前先清理缓存, 每次部署前先删除 .deploy 文件夹**
```

####复合命令
```
hexo deploy -g #生成加部署
hexo server -g #生成加预览
```

####简化命令
```
hexo n == hexo new
hexo g == hexo generate
hexo s == hexo server
hexo d == hexo deploy
```

####安装插件
```
npm install   --save #安装
npm update #升级
npm uninstall   #卸载
```

安装主题`<repository>`为主题的git仓库,`<theme-name>`为要存放在本地的目录名
```
git clone <repository> themes/<theme-name>
```
修改网站配置文件
```
theme:<theme-name>
```

### 编辑文章

#### 新建文章
```
hexo new 'post_name'
```
在post目录下会生成``post_name.md``文件
```
title: 文章标题
date: 2015-09-29 17:11:07 时间
categories: Hexo  分类
tags: 
 - Hexo        标签
permalink: 固定链接
---
正文
```

#### 发布文章

编辑全局配置文件`_config.yml`中的`deploy`部分, `zerocyl`为用户名


GitHub：
```
deploy:
  type: github
  repo: https://github.com/zerocyl/zerocyl.github.io.git
  branch: master
```
或者
```
deploy:
  type: github
  repository: git@github.com:zerocyl/zerocyl.github.com.git
  branch: master
```

GitCafe：将项目主页branch设置问gh-pages
```
deploy:
  type: git
  repository: git@gitcafe.com:zerocyl/zerocyl.git
  branch: gitcafe-pages
```

### 部署
```
hexo deploy
hexo d -g
```

如果出现以下提示表示部署成功
```
INFO  Deploy done: git
```

点击 Github 上项目的 Settings, GitHub Pages, 提示 *Your site is published at http://zerocyl.github.io/*第一次上传网站需要等十分钟左右, 以后每次更新都能马上打开

### 绑定域名

  如果不绑定域名只能通过*you_user_name.github.io*访问，我的域名是从*Godaddy*申请，域名解析采用*DNSPod*

绑定一级域名

主机记录*@*，类型*A*，记录值*192.30.252.154*
主机记录*www*，类型*A*，记录值*192.30.252.154*

可以参考[Tips for configuring an A record with your DNS provider](https://help.github.com/articles/tips-for-configuring-an-a-record-with-your-dns-provider/)这篇文章配置

绑定二级域名(我的域名是zerounix.com)

主机记录*blog*，类型*CNAME*，记录值*zerocyl.github.io*

*GitCafe绑定域名可以在项目管理界面，左侧导航栏中有自定义域名设置*

### 主题

Hexo的[主题列表](https://github.com/hexojs/hexo/wiki/Themes)

#### 下载安装主题
```
cd hexo-lcx
git clone https://github.com/iissnan/hexo-theme-next themes/next
```

也可以手动下载后解压到 themes 目录,全局配置文件 _config.yml 中 theme 改成 next


#### 主题配置文件
```
# when running hexo in a subdirectory (e.g. domain.tld/blog), remove leading slashes ( "/archives" -> "archives" )
menu:
  home: /
  categories: /categories
  tags: /tags
  archives: /archives
  about: /about
  #commonweal: /404.html

# Place your favicon.ico to /source directory.
favicon: /favicon.ico

# Set default keywords (Use a comma to separate)
keywords: "Hexo,next"

# Set rss to false to disable feed link.
# Leave rss as empty to use site's feed link.
# Set rss to specific value if you have burned your feed already.
rss:

# Icon fonts
# Place your font into next/source/fonts, specify directory-name and font-name here
# Avialable: default | linecons | fifty-shades | feather
#icon_font: default
#icon_font: fifty-shades
#icon_font: feather
icon_font: linecons

# Code Highlight theme
# Available value: normal | night | night eighties | night blue | night bright
# https://github.com/chriskempson/tomorrow-theme
highlight_theme: normal


# MathJax Support
mathjax:


# Schemes
scheme: Mist


# Sidebar, available value:
#  - post    expand on posts automatically. Default.
#  - always  expand for all pages automatically
#  - hide    expand only when click on the sidebar toggle icon.
sidebar: post
#sidebar: always
#sidebar: hide


# Automatically scroll page to section which is under <!-- more --> mark.
scroll_to_more: true


# Automatically add list number to toc.
toc_list_number: true

# Automatically Excerpt
auto_excerpt:
  enable: false
  length: 150

# Use Lato font
# Note: this option is avialable only when the language is not `zh-Hans`
use_font_lato: true

# Make duoshuo show UA
# user_id must NOT be null when admin_enable is true!
# you can visit http://dev.duoshuo.com get duoshuo user id.
duoshuo_info:
  ua_enable: true
  admin_enable: false
  user_id: 0

## DO NOT EDIT THE FOLLOWING SETTINGS
## UNLESS YOU KNOW WHAT YOU ARE DOING

# Use velocity to animate everything.
use_motion: true

# Fancybox
fancybox: true

# Static files
vendors: vendors
css: css
js: js
images: images

# Theme version
version: 0.4.4

```
#### 选择Scheme
````
scheme: Mist
````

#### 添加小图标favicon.ico
将 favicon.ico 文件放在 source 目录下, 修改主题配置文件
```
favicon: /favicon.ico
```

#### 语言设置

* English (en)
* 中文简体 (zh-Hans)
* French (fr-FR)
* 中文繁体 (zh-hk/zh-tw)
* Russian (ru)
* German (de)

站点配置文件
```
language:zh-hk
```
#### 菜单设置
编辑主题配置文件的 menu
若站点运行在子目录中, 将链接前缀的 `/` 去掉
```
menu:
 home: /
 archives: /archives
 categories: /categories
 tags: /tags
 commonweal: /404.html
 about: /about
```

#### 分类页面
添加一个分类页面，并在菜单中显示页面链接
新建`categories`页面
```
hexo new page "categories"
```
将页面的类型设置为`categories`
```
title: categories
date: 2015-10-09 16:33:59
type: categories
---
```
关闭评论增加`comments: false`

在菜单中添加链接. 编辑主题配置文件, 添加 `categories` 到 `menu` 中
```
menu:
  tags: /categories
```

#### 标签页面
添加一个标签页面，并在菜单中显示页面链接
新建`tags`页面
```
hexo new page "tags"
```
将页面的类型设置为`tags`
```
title: tags
date: 2015-10-09 16:33:59
type: tags
---
```
关闭评论增加`comments: false`

在菜单中添加链接. 编辑主题配置文件, 添加 `tags` 到 `menu` 中
```
menu:
  tags: /tags
```

下插件
```
hexo-generator-index
hexo-generator-archive
hexo-generator-tag
```
站点配置文章中设定
```
index_generator:
 per_page: 5
archive_generator:
 per_page: 20
 yearly: true
 monthly: true
tag_generator:
 per_page: 10
```
#### 自定义字体
编辑主题 `source/css/_variables/custom.styl` 文件, 例如
```
$font-family-headings = Georgia, sans
$font-family-base = "Microsoft YaHei", Verdana, sans-serif
```

#### 自定义页面内容区域的宽度
编辑主题 `source/css/_variables/custom.styl` 文件
```
$content-desktop = 700px
```

## 扩展应用

### 多说评论系统
登陆多说创建站点, 多说域名*xxx.duoshuo.com*前面的*xxx*即为*duoshuo_shortname*, 在站点配置文件中新增 *duoshuo_shortname*字段
```
duoshuo_shotname: xxx
```
如需取消某个页面/文章的评论, 在 md 文件的 front-matter 中增加 comments: false

多说评论组件提供热评文章功能, 仅在文章页面显示

站点/主题配置文件中设置增加
```
# 多说热评文章 true 或者 false
duoshuo_hotartical: true
```

### Disqus
---
在[Disqus](https://disqus.com/)官网申请*shotname*，在站点配置文件中，添加*disqus-shortname*
    
    disqus_shortname: xxxxxxxx

### 网站统计

#### 百度统计
登录[百度统计](http://tongji.baidu.com/web/welcome/login), 定位到站点的代码获取页面复制*hm.js?*后面那串统计脚本*id*编辑站点配置文件, 新增字段*baidu_analytics*字段

    baidu_analytics: xxxxxxxxxxxxxxxx

#### Google Analytics

从[Google Analytics](http://www.google.com/analytics/) 获取 ID站点配置文件新增 *google_analytics*, 设置成 Google 跟踪 ID. 通常是以 UA- 开头

    google_analytics: UA-xxxxxxxx-x

### 分享

####[JiaThis](http://www.jiathis.com/)

站点/主题配置文件添加字段*jiathis*, 值为*true*
```
# JiaThis 分享服务
jiathis: true
```

####[百度分享](http://share.baidu.com/)

站点/主题配置文件添加字段*baidushare*, 值为*true*
```
# 百度分享服务
baidushare: true
```

####[多说分享](http://duoshuo.com/)

站点/主题配置文件添加字段 duoshuo_share, 值为 true, 多说分享必须与多说评论同时使用
```
# 多说分享服务
duoshuo_share: true
```

### Swiftype 搜索

站点配置文件新增 swiftype_key 字段, 值为 swiftype 搜索引擎的 key
```
swiftype_key: xxxxxxxxx
Google Webmaster tools
```

### Google Webmaster tools

设置 Google 站点管理工具的验证字符串, 用于提交 sitemap

* 获取 google site verification code
 
* 登录 Google Webmaster Tools, 导航到验证方法, 并选择 HTML 标签, 将会获取到一段代码
```
<meta name="google-site-verification" content="XXXXXXXXXXXXXXXXXXXXXXX" />
```

* 将 content 里面的 XXXXXXXXXXXXXXXXXXXXXXX 复制出来, 站点配置文件新增字段`google_site_verification`
```
        google_site_verification google_site_verification: XXXXXXXXXXXXXXXXXXXXXXX
```

### 版权
参见[知识共享许可协议](https://zh.wikipedia.org/wiki/%E5%89%B5%E4%BD%9C%E5%85%B1%E7%94%A8%E6%8E%88%E6%AC%8A%E6%A2%9D%E6%AC%BE)
站点配置文件新增
```
# Creative Commons 4.0 International License.
# http://creativecommons.org/
# Available: by | by-nc | by-nc-nd | by-nc-sa | by-nd | by-sa | zero
creative_commons: by-nc-sa
```

### 图片显示
把图片放到 source/images 目录下
```
![test](images/xxx.jpg)
```
*推荐使用图床, 例如[七牛云存储](http://www.qiniu.com/)*

### 自定义 404 页面

添加 source/404.html

404 页面不需要 Hexo 解析
自定义 404 页面
添加 source/404.html
```
layout: false
--------
<!DOCTYPE html>
<html>
 <head>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 <title>404</title>
 <link rel="icon" href="/favicon.ico">
 </head>
 <body>
 <div align="center">
 <p>404 你懂的</p>
 </div>
 </body>
</html>
```

### 添加 robots.txt
source 目录下添加 robots.txt
```
# robots.txt
User-agent: Baiduspider
Disallow: /
User-agent: Googlebot
Disallow:
```
### 生成 post 时默认生成 categories 配置项

在 scaffolds/post.md 中添加
```
categories:
```
### 添加 “fork me on github”
[官方教程](https://github.com/blog/273-github-ribbons)

### 点击加载评论
在 `themes\next\layout\_layout.swig` 里找到
```
<div id="disqus_thread">
<noscript>Please enable JavaScript to view the <a href="//disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
</div>
```
在上面添加
```
<button id="load-disqus" onclick="disqus.load();" style="background-color: #ebebeb; color: #646464; font-size: 18px; padding: 8px 12px; border-radius: 5px; border: 1px solid #ebebeb;">点击查看评论</button>
```
修改文件
`themes\next\layout\_scripts\comments\disqus.swig`
```
<script type="text/javascript">

var disqus = { //添加的内容
load : function disqus(){ //添加的内容

 var disqus_shortname = '{{theme.disqus_shortname}}';
 var disqus_identifier = '{{ page.path }}';
 var disqus_title = '{{ page.title }}';
 var disqus_url = '{{ page.permalink }}';
 function run_disqus_script(disqus_script){
 var dsq = document.createElement('script');
 dsq.type = 'text/javascript';
 dsq.async = true;
 dsq.src = '//' + disqus_shortname + '.disqus.com/' + disqus_script;
 (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
 }
 run_disqus_script('count.js');
 {% if page.comments %}
 run_disqus_script('embed.js');
 {% endif %}

$('#load-disqus').remove(); //添加的内容
} //添加的内容
} //添加的内容

</script>
```

### 给 GitHub 添加 README

把 README.MD 文件的后缀名改成 MDOWN, 放到 source 文件夹下, 这样 Hexo 不会将其解析成网页, GitHub 也会作为 MD 文件解析

### 网站访问量统计

使用[不蒜子](http://service.ibruce.info/) 提供的服务

#### 安装脚本
```
<script async src="https://dn-lbstatics.qbox.me/busuanzi/2.3/busuanzi.pure.mini.js"></script>
```
>不蒜子可以给任何类型的个人站点使用，如果你是用的hexo，打开themes/你的主题/layout/_partial/footer.ejs添加上述脚本即可，当然你也可以添加到 header 中。


#### 安装标签

算法a: pv的方式, 单个用户连续点击n篇文章, 记录n次访问量.
```
<span id="busuanzi_container_site_pv">
 本站总访问量<span id="busuanzi_value_site_pv"></span>次
</span>
```

算法b: uv的方式, 单个用户连续点击n篇文章, 只记录1次访客数.
```
<span id="busuanzi_container_site_uv">
 本站访客数<span id="busuanzi_value_site_uv"></span>人次
</span>
```
>如果你是用的hexo，打开themes/你的主题/layout/_partial/footer.ejs添加即可。

### 网站运行时间
脚本：
```
<script>
var birthDay = new Date("11/20/2014");
var now = new Date();
var duration = now.getTime() - birthDay.getTime(); 
var total= Math.floor(duration / (1000 * 60 * 60 * 24));
document.getElementById("showDays").innerHTML = "本站已运行 "+total+" 天";
</script>
```

标签：
```
<span id="showDays"></span>
```

### 简体中文/繁体中文切换
下载[js](http://www.arao.me/js/tw_cn.js)文件 放到主题的*js*文件夹

添加标签
```
<a id="translateLink" href="javascript:translatePage();">繁體</a>
```

添加脚本
```
<script type="text/javascript" src="/js/tw_cn.js"></script>
<script type="text/javascript">
var defaultEncoding = 2; //网站编写字体是否繁体，1-繁体，2-简体
var translateDelay = 0; //延迟时间,若不在前, 要设定延迟翻译时间, 如100表示100ms,默认为0
var cookieDomain = "http://www.arao.me/"; //Cookie地址, 一定要设定, 通常为你的网址
var msgToTraditionalChinese = "繁體"; //此处可以更改为你想要显示的文字
var msgToSimplifiedChinese = "简体"; //同上，但两处均不建议更改
var translateButtonId = "translateLink"; //默认互换id
translateInitilization();
</script>
```

### Kill IE6

```
<!--[if IE 6]>
 <script src="//letskillie6.googlecode.com/svn/trunk/2/zh_CN.js"></script>
<![endif]-->
```

### 迁移
参考官方文档[Hexo Migration](http://zespia.tw/hexo/docs/migration.html)

### 更多信息
更多信息参考[官方文档](https://hexo.io/zh-cn/docs)
