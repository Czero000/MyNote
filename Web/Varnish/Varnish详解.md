# Varnish 入门
![varnish-logo](http://ofc9x1ccn.bkt.clouddn.com/varnish/varnish-bunny.png)

Varnish 是一款高性能且开源的反向代理服务器和 HTTP 加速器，其采用全新的软件体系机构，和现在的硬件体系紧密配合，与传统的 squid 相比，varnish 具有性能更高、速度更快、管理更加方便等诸多优点

## Varnish 介绍及工作原理
Varnish [官方网址http://www.varnish-cache.org/](http://www.varnish-cache.org/)。

当前最新版本[Varnish Cache 5.0](https://repo.varnish-cache.org/source/varnish-5.0.0.tar.gz)
当前稳定版本[Varnish Cache 4.1.3](https://repo.varnish-cache.org/source/varnish-4.1.3.tar.gz)

Varnish 不仅可以用于反向代理，根据使用方法的不同还可以应用于更多的场景。

- web application firewall, (Web应用防火墙)
- DDoS attack defender, (DDoS攻击防护)
- hotlinking protector,(网站防盗链)
- load balancer,(负载均衡)
- integration point,(不知道是什么)
- single sign-on gateway,(单点登录网关)
- authentication and authorization policy mechanism,(认证和认证授权)
- quick fix for unstable backends, and(后端主机快速修复)
- HTTP router.(HTTP路由)

Varnish 缓存策略的实现是通过 `VCL（Varnish Configuration Language）` 实现，VCL 的语法简单，继承了 C 语言的很多特性，使得 VCL 样式看起来很像 C 和 PELR 语言，VCL 配置文件也是通过 VCL 编译为 C 代码后继而执行，高效与生俱来。Varnish 已在各大型和轻量型应用场景中充分证明其能力。Varnish 开源产品全称为 `Varnish Cache`，同时提供功能更为强大齐全的商业套件，全称为 `Varnish Plus`。

## Varnish 设计思想
Varnis 的设计初衷就定义为高效和灵活，其设计原则更是面向当今流行前沿的 64 位服务器架构，而非 15 年前的老架构服务器或 32 位系统架构。Varnish 底层使用专为高性能服务设计的 epool 和 kqueue 调度机制，借助内核的强大功能解决复杂场景。设计原则总结如下：

- 解决企业实际问题;
- 只运行在现代 64 位硬件架构体系，不支持兼容老的服务器架构;
- 与内核协同工作;
- 通过 VCL 编译生成 C 语言程序和内核交互;
- 通过 VMOD 模块方式扩展程序;
- 其通过工作空间为导向的内存共享机制来减少锁争夺

## Object 对象存储机制

Object对象缓存按如下规则存储

- HTTP 响应信息缓存本地；
- Varnish 处理的对象在内存中以 hash 树方式存储；
- 用户可处理和控制 hash 信息；
- 多个对象可拥有相同的 hash 地址；

## Object对象存活时间
Varnish 基于内存缓存，众所周知，内存即使在现在也是非常昂贵的设备且容量有限，因此所有缓存对象均在缓存周期，过期数据或缓存策略内的数据会被清理。每个 Object 的生命周期分为如图4个阶段：
![object-lifetime](http://ofc9x1ccn.bkt.clouddn.com/varnish/object-lifetime.png)
每个对象拥有1个起初时间缀和3个时间属性，分别是1) TTL, 2) grace, and 3) keep. t_origin，其中：

- 对象缓存周期为 ：`t_origin->TTL->grace->keep`，之后 Object 将被从 Varnish 缓存中删除
- 对象新鲜期为：`t_origin->TTL`
- 对象陈旧期为：`TTL->grace`
- `If-Modified-Since` 属性周期为：`t_origin->TTL->grace->keep`

## 常见缓存工具 Varnish 与 Squid 的优缺点分析

介绍 Varnish 必然需提及缓存的开山鼻祖 Squid，Squid 是很古老的反向代理软件，拥有传统代理、身份验证、流量管理等高级功能，但是配置太复杂。优势在于完整的庞大的 cache 技术资料。Squid 在大规模负载均衡场景下很稳定。而相对老牌的 Squid 而言，Varnish 是新兴的一个软件，属于后起之秀，其设计简单，工作于内存，即数据缓存在内存中，因此重启后 Varnish 会发生数据的问题。

- Varnish & Squid 简要对比如下

| 软件    | 存储模式  | 性能   | 配置复杂度 | purge效率 | 共享存储       |
| ----- | ----- | ---- | ----- | ------- | ----------- |
| squid | 硬盘    | 较高   | 简单    | 低   | 可以并联，但是配置复杂 |
| varnish| 硬盘/内存 | 高    | 比较简单  | 低 |不能|

- Varnish 与 Squid 相同点
  - 都是一个反向代理服务器；
  - 都是开源软件；

- Varnish 对比 Squid 的优点
  - varnish 稳定性很高，两者在完成相同负荷的工作时，squid 服务器发生故障的几率要高于 varnish,因为 squid 要经常重启;
  - varnish 访问速度更快，其采用了 ”Visual Page Cache” 技术，所有缓存数据都直接从内存中读取，而 squid 是从硬盘读取，因而 varnish 在访问速度方面会更快;
  - varnish 可支持更多并发连接，因为 varnish 的 TCP 连接释放要比 squid 快，因而在高并发连接情况下可以支持更多 TCP 连接;
  - varnish 可以通过管理端口，使用正则表达式批量的清除部分缓存，而 squid 是做不到的;
  - squid 属于单进程使用单核 CPU，但 Varnish 是通过 fork 形式打开多进程来做处理，所以是合理的使用所有核来处理相应的请求;

- Varnish 对比 Squid 的缺点
  - varnish 进程一旦 Hang、Crash 或者重启，缓存数据都会从内存中完全释放，此时所有请求都会发送到后端服务器，在高并发情况下，会给后端服务器造成很大的压力;
  - 在 varnish 使用中，如果单个 url 的请求通过 HA/F5，每次请求不同的 varnish 服务器时，被请求的 varnish 服务器都会被穿透到后端，而同样的请求会在多台服务器上缓存 ，也会造成varnish的缓存资源浪费，也会造成性能下降;

- Varnish劣势的解决方案
  - 针对劣势一：在访问量很大的情况下推荐使用 varnish 的内存缓存方式启动，而且后面需要跟多台 squid 服务器。主要为了防止前面的 varnish 服务、服务器被重启的情况下，大量请求穿透 varnish，这样 squid 可以就担当第二层 CACHE，而且也弥补了varnish 缓存在内存中重启都会释放的问题；
  - 针对劣势二：可以在负载均衡上做 url 哈希，让单个 url 请求固定请求到一台 varnish 服务器上;

## 对比Varnish 3.x的主要改进
- 完全支持流对象；
- 可后台获取失效的对象，即 Client/backend分离；
- 新的 vanishlog 查询语言，允许对请求进行自动分组；
- 复杂的请求时间戳和字节计数；
- 安全方面的提升；

## 涉及VCL语法的改变点
- vcl 配置文件需明确指定版本：即在vcl文件的第一行写上 vcl 4.0;
- vcl_fetch 函数被 vcl_backend_response 代替，且`req.*`不再适用vcl_backend_response；
- 后端源服务器组director成为varnish模块，需 import directors 后再在 vcl_init 子例程中定义；
- 自定义的子例程(即一个sub)不能以vcl_开头，调用使用call sub_name；
- error()函数被synth()替代；
- return(lookup)被return(hash)替代；
- 使用beresp.uncacheable创建hit_for_pss对象；
- 变量req.backend.healty被std.healthy(req.backend)替代；
- 变量req.backend被req.backend_hint替代；
- 关键字remove被unset替代；
详见：[https://www.varnish-cache.org/docs/4.0/whats-new/index.html#whats-new-index](https://www.varnish-cache.org/docs/4.0/whats-new/index.html#whats-new-index)

## 架构及文件缓存的工作流程
![](http://ofc9x1ccn.bkt.clouddn.com/varnish/cache-workflow.jpg)
- Varnish 分为 master 进程和 child 进程；
- Master 进程读入存储配置文件，调用合适的存储类型，然后创建 / 读入相应大小的缓存文件，接着 master 初始化管理该存储空间的结构体，然后 fork 并监控 child 进程；
- Child 进程在主线程的初始化的过程中，将前面打开的存储文件整个 mmap 到内存中，此时创建并初始化空闲结构体，挂到存储管理结构体，以待分配；
- 对外管理接口分为3种，分别是命令行接口、Telnet接口和Web接口；
- 同时在运行过程中修改的配置，可以由VCL编译器编译成C语言，并组织成共享对象(Shared Object)交由Child进程加载使用；

![](http://ofc9x1ccn.bkt.clouddn.com/varnish/childprocess.jpg)
Child 进程分配若干线程进行工作，主要包括一些管理线程和很多 worker 线程，可分为：
- Accept线程：接受请求，将请求挂在overflow队列上；
- Work线程：有多个，负责从overflow队列上摘除请求，对请求进行处理，直到完成，然后处理下一个请求；
- Epoll线程：一个请求处理称为一个session，在session周期内，处理完请求后，会交给Epoll处理，监听是否还有事件发生；
- Expire线程：对于缓存的object，根据过期时间，组织成二叉堆，该线程周期检查该堆的根，处理过期的文件，对过期的数据进行删除或重取操作；

## HTTP请求基本处理流程
![](http://ofc9x1ccn.bkt.clouddn.com/varnish/http-request-workflow.jpg)
- Receive 状态（vcl_recv）：也就是请求处理的入口状态，根据 VCL 规则判断该请求应该 pass（vcl_pass）或是 pipe（vcl_pipe），还是进入 lookup（本地查询）；
- Lookup 状态：进入该状态后，会在 hash 表中查找数据，若找到，则进入 hit（vcl_hit）状态，否则进入 miss（vcl_miss）状态；
- Pass（vcl_pass）状态：在此状态下，会直接进入后端请求，即进入 fetch（vcl_fetch）状态；
- Fetch（vcl_fetch）状态：在 fetch 状态下，对请求进行后端获取，发送请求，获得数据，并根据设置进行本地存储；
- Deliver（vcl_deliver）状态：将获取到的数据发给客户端，然后完成本次请求；
注：Varnish4中在vcl_fetch部分略有出入，已独立为vcl_backend_fetch和vcl_backend_response2个函数；

## 内置函数(也叫子例程)
- vcl_recv：用于接收和处理请求；当请求到达并成功接收后被调用，通过判断请求的数据来决定如何处理请求；
- vcl_pipe：此函数在进入pipe模式时被调用，用于将请求直接传递至后端主机，并将后端响应原样返回客户端；
- vcl_pass：此函数在进入pass模式时被调用，用于将请求直接传递至后端主机，但后端主机的响应并不缓存直接返回客户端；
- vcl_hit：在执行 lookup 指令后，在缓存中找到请求的内容后将自动调用该函数；
- vcl_miss：在执行 lookup 指令后，在缓存中没有找到请求的内容时自动调用该方法，此函数可用于判断是否需要从后端服务器获取内容；
- vcl_hash：在vcl_recv调用后为请求创建一个hash值时，调用此函数；此hash值将作为varnish中搜索缓存对象的key；
- vcl_purge：pruge操作执行后调用此函数，可用于构建一个响应；
- vcl_deliver：将在缓存中找到请求的内容发送给客户端前调用此方法；
- vcl_backend_fetch：向后端主机发送请求前，调用此函数，可修改发往后端的请求；
- vcl_backend_response：获得后端主机的响应后，可调用此函数；
- vcl_backend_error：当从后端主机获取源文件失败时，调用此函数；
- vcl_init：VCL加载时调用此函数，经常用于初始化varnish模块(VMODs)
- vcl_fini：当所有请求都离开当前VCL，且当前VCL被弃用时，调用此函数，经常用于清理varnish模块；

## VCL中内置公共变量
变量(也叫object)适用范围
![](http://ofc9x1ccn.bkt.clouddn.com/varnish/vcl-variables.jpg)

## 变量类型详解
![](http://ofc9x1ccn.bkt.clouddn.com/varnish/http-variable.jpg)

- req：The request object，请求到达时可用的变量
- bereq：The backend request object，向后端主机请求时可用的变量
- beresp：The backend response object，从后端主机获取内容时可用的变量
- resp：The HTTP response object，对客户端响应时可用的变量
- obj：存储在内存中时对象属性相关的可用的变量
具体变量详见：https://www.varnish-cache.org/docs/4.0/reference/vcl.html#reference-vcl


# Varnish配置进阶
了解完Varnish的功能作用，优劣势及在企业技术架构中扮演的角色后，我们接着了解Varnish工具套件。熟练掌握这些工具的功能作用及使用对于Varnish的应用很有帮助。

## Varnish核心工具集介绍

### varnishd
varnishd是varnish的核心进程，以Daemon方式运行，接受HTTP请求，转发前端请求至后端backend，缓存返回的缓存对象并且回应请求的客户端。

### varnishtest
- 验证Varnish的安装
- 功能强大，可自定义client请求模型或从后端真实用品拉取内容。
- 支持与Varnish交互性

### varnishadm Varnish实例命令行管理工具
- start/stop Varnishd
- 更新配置文件参数
- 重载Varnish Configuration Language(VCL)
- 查看最新的参数文档

### varnishlog
- Varnish日志展示工具，因信息量较大往往需要事先过滤。varnishlog支持精确日志匹配。

### varnishstat
varnishstat可访问全局计算器，可提供全面的统计信息，如全部请求数，缓存对象的数量等。常和varnishlog结合分析Varnish的安装。

###其它工具
varnishncsa、varnishtop、varnishhist对Varnish的性能及状态分析均有帮助。

---

##  Varnish 安装部署

### 系统环境
| Roles    | ip  | Detail  
| ----- | ----- | ---- |
| varnish(4.1.3) | 172.16.11.211 |80|
| WebServer(nginx)| 172.16.11.210 |80|

### 安装
```
// 源码安装
wget https://repo.varnish-cache.org/source/varnish-4.1.3.tar.gz
tar -zxf varnish-4.1.3.tar.gz
cd varnish-4.1.3
make && make install
```

### 配置
配置文件及启动脚本是根据 yum 形式安装后生成的有下面几个文件
- default.vcl            // Vcl 配置模板
- varnish.params         // varnish 变量文件
- secret                 // 密码文件
- varnish                // 日志切割
- varnishlog.service     // systemd 文件
- varnishncsa.service    // systemd 文件  
- varnish.service        // systemd 文件

[配置文件](http://ofc9x1ccn.bkt.clouddn.com/varnish/varnish-cfg.tar.gz)

简单配置示例

1. 更改 varnish 默认监听端口
```
// 编辑 varnish.params
// 更改监听的 ip 和端口
VARNISH_LISTEN_ADDRESS=172.16.11.211
VARNISH_LISTEN_PORT=80
```
2. 修改 VCL backend 区块
```
// 编辑 default.vcl
backend default {
    .host = "172.16.11.210";
    .port = "80";
}
```
3. 启动服务
```
systemctl start varnish
```

4. 后端 web 服务健康检测
```
vim health_check.vcl
probe backend_healthcheck {
    .interval = 5s;
    .timeout = 3s;
    .window = 10;
    .threshold = 8;

    .request =
    "GET /index.html HTTP/1.1"
    "Host: mycheckweb.mytest.com"
    "Connection: close"
    "Accept-Encoding: foo/bar";
```

5. 后端 web 服务 定义
```
vim /usr/local/varnish/etc/hosts/10.160.22.88_8080.conf
backend WEBSRV_10_160_22_88_8080 {
    .host = "10.160.22.88";
    .port = "8080";

    .connect_timeout = 50s;
    .between_bytes_timeout = 30s;
    .first_byte_timeout = 30s;

    .probe = backend_healthcheck;
}
```

```
vim /usr/local/varnish/etc/hosts/10.173.146.35_8080.conf
backend WEBSRV_10_173_146_35_8080 {
    .host = "10.173.146.35";
    .port = "8080";

    .connect_timeout = 50s;
    .between_bytes_timeout = 30s;
    .first_byte_timeout = 30s;

    .probe = backend_healthcheck;
}
```
6. 集群定义
```
 vim /usr/local/varnish/etc/varnish.vcl
 include "/usr/local/varnish/etc/cluster.vcl";

acl allow_purge_cache {
    "127.0.0.1";
    "10.0.0.0"/8;
    "172.0.0.0"/8;
}

sub vcl_recv {
    if (req.request == "PURGE") {
        if (!client.ip ~ allow_purge_cache) {
            error 405 "Not Allowed.";
        }

        return (lookup);
    }

    if (req.http.host ~ "^(.*).mytest.com") {
        set req.backend = CLUSTER_BACKEND_SERVER;
    }

    ## 动态资源直接抛到后端服务器
    if (req.url ~ "\.(php|asp|aspx|jsp|do|ashx|shtml)($|\?)") {
        return (pass);
    }

    ## 静态资源需要去除cookie信息
    if (req.request == "GET" && req.url ~ "\.(css|js|bmp|png|gif|jpg|jpeg|ico|gz|tgz|bz2|tbz|zip|rar|mp3|mp4|ogg|swf|flv)($|\?)") {
        unset req.http.cookie;
        return (lookup);
    }

    if (req.restarts == 0) {
        if (req.http.x-forwarded-for) {
            set req.http.X-Forwarded-For = req.http.X-Forwarded-For + ", " + client.ip;
        } else {
            set req.http.X-Forwarded-For = client.ip;
        }
    }

    if (req.http.Cache-Control ~ "no-cache") {
        return (pass);
    }

    if (req.request != "GET" &&
        req.request != "HEAD" &&
        req.request != "PUT" &&
        req.request != "POST" &&
        req.request != "TRACE" &&
        req.request != "OPTIONS" &&
        req.request != "DELETE") {
        return (pipe);
    }

    if (req.request != "GET" && req.request != "HEAD") {
        return (pass);
    }

    if (req.http.Authorization || req.http.Cookie) {
        return (pass);
    }

    ## 静态资源压缩
    if (req.http.Accept-Encoding) {
        if (req.url ~ "\.(bmp|png|gif|jpg|jpeg|ico|gz|tgz|bz2|tbz|zip|rar|mp3|mp4|ogg|swf|flv)$") {
            remove req.http.Accept-Encoding;
        } elseif (req.http.Accept-Encoding ~ "gzip") {
            set req.http.Accept-Encoding = "gzip";
        } elseif (req.http.Accept-Encoding ~ "deflate") {
            set req.http.Accept-Encoding = "deflate";
        } else {
            remove req.http.Accept-Encoding;
        }
    }

    ## 防盗链设置
    if (req.http.referer ~ "http://.*") {
        if (!(req.http.referer ~ "http://.*\.qq\.com" ||
            req.http.referer ~ "http://.*\.baidu\.com" ||
            req.http.referer ~ "http://.*\.google\.com.*" ||
            req.http.referer ~ "http://.*\.sogou\.com" ||
            req.http.referer ~ "http://.*\.soso\.com" ||
            req.http.referer ~ "http://.*\.so\.com")) {
            set req.http.host = "www.mytest.com";
            set req.url = "/";
        }
    }

    if (!req.backend.healthy) {
        unset req.http.Cookie;
    }

    ## 跳过缓存大文件
    if (req.http.x-pipe && req.restarts > 0) {
        unset req.http.x-pipe;
        return (pipe);
    }

    ## 若backend是健康的，则仅grace 5s，如果backend不健康，则grace 1m，主要用于提高并发时的吞吐率
    if (req.backend.healthy) {
        set req.grace = 5s;
    } else {
        set req.grace = 1m;
    }
}

sub vcl_pipe {
    return (pipe);
}

sub vcl_pass {
    if (req.request == "PURGE") {
        error 502 "PURGE on a passed object";
    }
}

sub vcl_hash {
    hash_data(req.url);

    if (req.http.host) {
        hash_data(req.http.host);
    } else {
        hash_data(server.ip);
    }

    if (req.http.Accept-Encoding ~ "gzip") {
        hash_data("gzip");
    } elseif (req.http.Accept-Encoding ~ "deflate") {
        hash_data("deflate");
    }

    return (hash);
}

sub vcl_hit {
    if (req.request == "PURGE") {
        purge;
        error 200 "Purged.";
    }
}

sub vcl_miss {
    if (req.request == "PURGE") {
        purge;
        error 404 "Purged.";
    }
}

sub vcl_fetch {
    ## 确保所有Cache中的内容在TTL过期后5分钟内不被删除，以应对高并发的场合
    set beresp.grace = 5m;

    if (beresp.http.Set-Cookie) {
        return (hit_for_pass);
    }

    ## 如果返回头有Cache-Control，则删除Set-Cookie头
    if (beresp.http.Cache-Control && beresp.ttl > 0s) {
        set beresp.grace = 1m;
        unset beresp.http.Set-Cookie;
    }

    ## 不缓存大于10MB的资源文件
    if (beresp.http.Content-Length ~ "[0-9]{8,}") {
        set req.http.x-pipe = "1";
        return (restart);
    }

    if (req.url ~ "\.(php|asp|aspx|jsp|do|ashx|shtml)($|\?)") {
        return (hit_for_pass);
    }

    if (req.request == "GET" && req.url ~ "\.(css|js|bmp|png|gif|jpg|jpeg|ico|gz|tgz|bz2|tbz|zip|rar|mp3|mp4|ogg|swf|flv)($|\?)") {
        unset beresp.http.set-cookie;
    }

    ## 如果返回头没有Cache-Control，则标记为hit_for_pass，强制后续请求回源
    if ((!beresp.http.Cache-Control && !beresp.http.Expires) ||
         beresp.http.Pragma ~ "no-cache" ||
         beresp.http.Cache-Control ~ "(no-cache|no-store|private)") {
        set beresp.ttl = 120s;
        return (hit_for_pass);
    }

    if (beresp.ttl <= 0s || beresp.http.Set-Cookie || beresp.http.Vary == "*") {
        set beresp.ttl = 120s;
        return (hit_for_pass);
    }

    ## 对不同类型静态资源进行缓存时间设置
    if (req.request == "GET" && req.url ~ "\.(css|js|bmp|png|gif|jpg|jpeg|ico)($|\?)") {
        set beresp.ttl = 15m;
    } elseif (req.request == "GET" && req.url ~ "\.(gz|tgz|bz2|tbz|zip|rar|mp3|mp4|ogg|swf|flv)($|\?)") {
        set beresp.ttl = 30m;
    } else {
        set beresp.ttl = 10m;
    }

    return (deliver);
}

sub vcl_deliver {
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT from " + req.http.host;
        set resp.http.X-Cache-Hits = obj.hits;
    } else {
        set resp.http.X-Cache = "MISS from " + req.http.host;
    }

    ## 去掉不必要的头信息
    unset resp.http.X-Powered-By;
    unset resp.http.Server;

    unset resp.http.Via;
    unset resp.http.X-Varnish;

    unset resp.http.Age;
}

sub vcl_error {
    if (obj.status == 503 && req.restarts < 5) {
        set obj.http.X-Restarts = req.restarts;
        return (restart);
    }
}

sub vcl_init {
    return (ok);
}

sub vcl_fini {
    return (ok);
}
```

7. Varnish启动参数配置文件
```
vim /usr/local/varnish/etc/varnish.conf
#!/bin/bash
#
# reload vcl revisited
# A script that loads new vcl based on data from /usr/local/varnish/etc/varnish.conf
# Ingvar Hagelund <ingvar@redpill-linpro.com>
#
# This is free software, distributed under the standard 2 clause BSD license,
# see the LICENSE file in the Varnish documentation directory
#
# The following environment variables have to be set:
# RELOAD_VCL, VARNISH_VCL_CONF, VARNISH_ADMIN_LISTEN_PORT
# The following are optional:
# VARNISH_SECRET_FILE, VARNISH_ADMIN_LISTEN_ADDRESS
#
# Requires GNU bash and GNU date
#

debug=false

missing() {
    echo "Missing configuration variable: $1"
    exit 2
}

print_debug() {
    echo "
Parsed configuration:
RELOAD_VCL=\"$RELOAD_VCL\"
VARNISH_VCL_CONF=\"$VARNISH_VCL_CONF\"
VARNISH_ADMIN_LISTEN_ADDRESS=\"$VARNISH_ADMIN_LISTEN_ADDRESS\"
VARNISH_ADMIN_LISTEN_PORT=\"$VARNISH_ADMIN_LISTEN_PORT\"
VARNISH_SECRET_FILE=\"$VARNISH_SECRET_FILE\"
"
}

# Read configuration
. /usr/local/varnish/etc/varnish.conf

$debug && print_debug

# Check configuration
if [ ! "$RELOAD_VCL" = "1" ]; then
    echo "Error: RELOAD_VCL is not set to 1"
    exit 2

elif [ -z "$VARNISH_VCL_CONF" ]; then
    echo "Error: VARNISH_VCL_CONF is not set"
    exit 2

elif [ ! -s "$VARNISH_VCL_CONF" ]; then
    echo "Eror: VCL config $VARNISH_VCL_CONF is unreadable or empty"
    exit 2

elif [ -z "$VARNISH_ADMIN_LISTEN_ADDRESS" ]; then
    echo "Warning: VARNISH_ADMIN_LISTEN_ADDRESS is not set, using 127.0.0.1"
    VARNISH_ADMIN_LISTEN_ADDRESS="127.0.0.1"

elif [ -z "$VARNISH_ADMIN_LISTEN_PORT" ]; then
    echo "Error: VARNISH_ADMIN_LISTEN_PORT is not set"
    exit 2

#elif [ -z "$VARNISH_SECRET_FILE" ]; then
#   echo "Warning: VARNISH_SECRET_FILE is not set"
#   secret=""

#elif [ ! -s "$VARNISH_SECRET_FILE" ]; then
#   echo "Error: varnish secret file $VARNISH_SECRET_FILE is unreadable or empty"
#   exit 2
else
#   secret="-S $VARNISH_SECRET_FILE"
    echo
fi

# Done parsing, set up command
#VARNISHADM="varnishadm $secret -T $VARNISH_ADMIN_LISTEN_ADDRESS:$VARNISH_ADMIN_LISTEN_PORT"
VARNISHADM="/usr/local/varnish/bin/varnishadm -T $VARNISH_ADMIN_LISTEN_ADDRESS:$VARNISH_ADMIN_LISTEN_PORT"

# Now do the real work
new_config="reload_$(date +%FT%H:%M:%S)"

# Check if we are able to connect at all
if $VARNISHADM vcl.list > /dev/null; then
    $debug && echo vcl.list succeeded
else
    echo "Unable to run $VARNISHADM vcl.list"
    exit 1
fi

if $VARNISHADM vcl.list | awk ' { print $3 } ' | grep -q $new_config; then
    echo Trying to use new config $new_config, but that is already in use
    exit 2
fi

current_config=$( $VARNISHADM vcl.list | awk ' /^active/ { print $3 } ' )

echo "Loading vcl from $VARNISH_VCL_CONF"
echo "Current running config name is $current_config"
echo "Using new config name $new_config"

if $VARNISHADM vcl.load $new_config $VARNISH_VCL_CONF; then
    $debug && echo "$VARNISHADM vcl.load succeded"
else
    echo "$VARNISHADM vcl.load failed"
    exit 1
fi

if $VARNISHADM vcl.use $new_config; then
    $debug && echo "$VARNISHADM vcl.use succeded"
else
    echo "$VARNISHADM vcl.use failed"
    exit 1
fi

$VARNISHADM vcl.list
echo Done

exit 0
```

8. varnish 启动脚本

```
#!/bin/bash
#
# varnish Control the Varnish Cache
#
# chkconfig: - 90 10
# description: Varnish is a high-perfomance HTTP accelerator
# processname: varnishd
# config: /usr/local/varnish/etc/varnish.conf
# PIDFILE: /var/run/varnishd.pid
#
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

BINFILE="/usr/local/varnish/sbin/varnishd"
PROG="varnishd"

RETVAL=0

GFILE="/usr/local/varnish/etc/varnish.conf"
PIDFILE="/var/run/varnish.pid"
LOCKFILE="/var/lock/varnish.lock"
RELOAD_EXEC="/usr/local/varnish/sbin/varnish_reload_vcl"

[[ -e ${GFILE} ]] && . ${GFILE}

start() {
    IS_EXIST=`ps -A -oppid,pid,cmd | grep sbin/${PROG} | grep -v grep`
    [[ -n "${IS_EXIST}" ]] && echo "The process of ${PROG} has been running." && exit 1

    [[ ! -x ${BINFILE} ]] && echo ${BINFILE} has no found && exit 5
    [[ ! -f ${GFILE} ]] && echo ${GFILE} has no found && exit 6

    echo -n "Starting Varnish Cache......"

    ulimit -n ${NFILES:-131072}
    ulimit -l ${MEMLOCK:-82000}
    ulimit -u ${NPROCS:-unlimited}

    if [[ "${DAEMON_OPTS}X" == "X" ]]; then
        echo -n "Please setting DAEMON_OPTS options in ${GFILE}"
        RETVAL=6
    else
        VARNISH_CACHE_DIR=`dirname $VARNISH_STORAGE_FILE`
        RETVAL=`grep -w '^VARNISH_STORAGE' ${GFILE} | grep malloc`
        if [[ "${RETVAL}X" = "X" ]]; then
            mkdir -p ${VARNISH_CACHE_DIR} && chown -R nobody:nogroup ${VARNISH_CACHE_DIR}
        else
            [[ -e ${VARNISH_CACHE_DIR} ]] && rm -rf ${VARNISH_CACHE_DIR}
        fi

        ${BINFILE} -P ${PIDFILE} $DAEMON_OPTS >/dev/null 2>&1
        RETVAL=$?
        echo
        [[ $RETVAL -eq 0 ]] && touch ${LOCKFILE}
    fi

    return $RETVAL
}

stop() {
    echo -n "Stopping Varnish Cache......"
    /sbin/killproc -QUIT ${PROG}
    RETVAL=$?
    echo
    [[ $RETVAL -eq 0 ]] && rm -f ${LOCKFILE}

    return $RETVAL
}

restart() {
    stop
    sleep 1
    start
}

reload() {
    [[ "$RELOAD_VCL" = "1" ]] && $RELOAD_EXEC || restart

    RETVAL=$?
    echo

    return $RETVAL
}

configtest() {
    if [[ -f ${GFILE} ]]; then
        ${BINFILE} -f ${GFILE} -C -n /tmp >/dev/null 2>&1
        RETVAL=$?
        [[ $? -eq 0 ]] && echo "The syntax is ok." || echo "The syntax is error."
    else
        RETVAL=$?
        echo "The config file: ${GFILE} is no exists."
    fi

    return $RETVAL
}

case "$1" in
start|stop|restart|reload|configtest)
    $1
    ;;

*)
    echo "Usage: $0 {start|stop|restart|reload|configtest}"
    exit 2
esac
                                                                                                                                                                                                                                                                                                                                                                                                               
exit $RETVAL
```

10. Varnish服务健康检查脚本
```
vim /usr/local/varnish/sbin/check_varnish_health.sh
#!/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin:/usr/local/sbin

## varnish启动参数配置文件
VARNISH_CONFIG="/usr/local/varnish/etc/varnish.conf"

IS_DEBUG=false

[[ -e ${VARNISH_CONFIG} ]] && . ${VARNISH_CONFIG}

${IS_DEBUG} && echo "监听地址：${VARNISH_LISTEN_ADDRESS}  监听端口：${VARNISH_LISTEN_PORT}"
LAN_IPADDR=`/sbin/ifconfig eth1 | awk -F ':' '/inet addr/{print $2}' | sed 's/[a-zA-Z ]//g'`

RETVAL=`nmap --system-dns -sT -p ${VARNISH_LISTEN_PORT} ${LAN_IPADDR} | grep open`
[[ -z ${RETVAL} ]] && /sbin/service varnishd restart >/dev/null 2>&1


// crontab
crontab -e
*/5 * * * * /usr/local/varnish/sbin/check_varnish_health.sh >/dev/null 2>&1
```
