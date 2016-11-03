![HTTPS_Title](https://czero000.github.io/nginx/https_title.jpg)

## HTTPS ##
HTTPS目前已经是所有重视隐私和安全性的网站的首选，例如国外的Google、Facebook、Twitter，国内则是淘宝、百度、京东等都已都支持了全站HTTPS，可以想象以下，如果一个网站没有加密，那么你的所有账户密码都是通过明文来传输，当涉及到隐私和金融问题，不加密是多么可怕的事情。

随着技术的发展，HTTPS网站已不再是大型网站的专利，所有普通的个人站点和blog可以以自己动手搭建一个安全加密的网站。

### 什么是HTTPS、SSL证书###

* HTTPS

> 超文本传输安全协议（缩写：HTTPS，英语：Hypertext Transfer Protocol Secure）是超文本传输协议和SSL/TLS的组合，用以提供加密通讯及对网络服务器身份的鉴定。HTTPS连接经常被用于万维网上的交易支付和企业信息系统中敏感信息的传输。HTTPS不应与在RFC 2660中定义的安全超文本传输协议（S-HTTP）相混。

* SSL证书

SSL证书是数字证书的一种，遵守SSL协议，使用 Secure Socket Layer 协议在浏览器和 Web 服务器之间建立一条安全通道，从而实现数据信息在客户端和服务器之间的加密传输，保证双方传递信息的安全性，不可被第三方窃听；用户可以通过服务器证书验证他所访问的网站是否真实可靠。

等多关于HTTPS、SSl证书的信息，请Google.

## 使用OpenSSL 生成自签名证书 ##

### 制作CA证书 ###
* 修改CA配置文件

```
vim /etc/pki/tls/openssl.conf
[ CA_default ]

dir             = /etc/pki/CA           # Where everything is kept
certs           = $dir/certs            # Where the issued certs are kept
crl_dir         = $dir/crl              # Where the issued crl are kept
database        = $dir/index.txt        # database index file.
#unique_subject = no                    # Set to 'no' to allow creation of
                                        # several ctificates with same subject.
new_certs_dir   = $dir/newcerts         # default place for new certs.

certificate     = $dir/cacert.pem       # The CA certificate
serial          = $dir/serial           # The current serial number
crlnumber       = $dir/crlnumber        # the current crl number
                                        # must be commented out to leave a V1 CRL
crl             = $dir/crl.pem          # The current CRL
private_key     = $dir/private/cakey.pem# The private key
RANDFILE        = $dir/private/.rand    # private random number file


default_days    = 3650                   # how long to certify for

[ policy_match ]
countryName             = match
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional


[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = CN
countryName_min                 = 2
countryName_max                 = 2


stateOrProvinceName             = State or Province Name (full name)
stateOrProvinceName_default     = BJ
```

* 在CA目录下创建两个初始文件

```
touch index.txt serial
echo 01 > serial
```

* 生成根密钥

```
cd /etc/pki/CA/
(umask 077; openssl genrsa -out private/cakey.pem 2048 )
```

* 生成根证书

```
(umask 077;openssl req -new -x509 -key private/cakey.pem -out cacert.pem)
```
会提示输入一些内容，因为是私有的，所以可以随便输入（之前修改的openssl.cnf会在这里呈现），最好记住能与后面保持一致。上面的自签证书`cacert.pem`应该生成在`/etc/pki/CA`下


### 制作服务器证书 ###

* 生成服务器ssl密钥

```
mkdir /usr/local/nginx/ssl
cd /usr/local/nginx/ssl
openssl genrsa -out nginx.key 2048
```

* 为ningx生成证书签署请求

```
// 同样会提示输入一些内容，其它随便，除了`Commone Name`一定要是你要授予证书的服务器域名或主机名，challenge password不填。
openssl req -new -key nginx.key -out nginx.csr
```

* 用私有CA来签署证书

```
openssl ca -in nginx.csr -out nginx.crt
Using configuration from /etc/pki/tls/openssl.cnf
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 1 (0x1)
        Validity
            Not Before: Feb  5 07:17:48 2016 GMT
            Not After : Feb  2 07:17:48 2026 GMT
        Subject:
            countryName               = CN
            stateOrProvinceName       = BJ
            localityName              = BJ
            organizationName          = Default Company Ltd
            commonName                = *.zerounix.com
        X509v3 extensions:
            X509v3 Basic Constraints: 
                CA:FALSE
            Netscape Comment: 
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier: 
                18:A2:A4:B8:69:03:23:FE:94:7C:D8:95:A8:B9:95:B6:E7:28:D7:58
            X509v3 Authority Key Identifier: 
                keyid:0D:01:60:ED:AF:82:A6:DB:46:42:BB:D7:F5:BD:4C:22:B8:6E:9F:33

Certificate is to be certified until Feb  2 07:17:48 2026 GMT (3650 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated

另外在极少数情况下，上面的命令生成的证书不能识别，试试下面的命令：
openssl x509 -req -in server.csr -CA /etc/pki/CA/cacert.pem -CAkey /etc/pki/CA/private/cakey.pem -CAcreateserial -out server.crt
```
上面签发过程其实默认使用了`-cert cacert.pem -keyfile cakey.pem`，这两个文件就是前两步生成的位于`/etc/pki/CA`下的根密钥和根证书。将生成的crt证书发回nginx服务器使用。


* 精简上面的步骤如下

```
mkdir /usr/local/ngnix/ssl
cd /usr/lcoal/nginx/ssl
// 创建根证书私钥
openssl genrsa -des3 -out ca.key 2048
// 创建根证书 (这里/C表示国家(Country)，只能是国家字母缩写，如CN、US等；/ST表示州或者省(State/Provice)；/L表示城市或者地区(Locality)；/O表示组织名(Organization Name)；/OU其他显示内容，一般会显示在颁发者这栏)
openssl req -new -x509 -days 36500 -key ca.key -out ca.crt -subj "/C=CN/ST=BeiJing/L=BeiJing/O=Your Company Name/OU=Your Root CA"
// 创建服务器ssl证书私钥
openssl genrsa -des3 -out server.key 2048
// 建立SSL证书(/O字段内容必须与刚才的CA根证书相同；/CN字段为公用名称(Common Name)，必须为网站的域名(不带www)；/OU字段最好也与为网站域名，当然选择其他名字也没关系)
openssl req -new -key server.key -out server.csr -subj "/C=CN/ST=BeiJing/L=BeiJing/O=Your Company Name/OU=zerounix.com/CN=zerounix.com"
// 准备
mkdir demoCA
cd demoCA
mkdir newcerts
touch index.txt
echo '01' > serial
cd ..
// 自签名证书
openssl ca -in server.csr -out server.crt -cert ca.crt -keyfile ca.key
```
更为简单的步骤
```
openssl genrsa -des3 -out server.key 2048
openssl req -new -key server.key -out server.csr 
```


## 配置Nginx支持SSL ##

### 编辑配置文件 ###
```
server {
    listen 443 ssl;
    server_name www.zerounix.com;
    root /data/website/www.zerounix.com;
    charset utf-8;
    index index.php index.html;
    ssl on;                                                    // 开启ssl支持
    ssl_certificate      /usr/local/nginx/ssl/nginx.crt;       // 证书位置
    ssl_certificate_key  /usr/local/nginx/ssl/nginx.key;       // 私钥
    ssl_session_timeout  5m;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;                  // 指定密码为openssl支持的格式
    ssl_ciphers         HIGH:!aNULL:!MD5;                      // 加密方法
    ssl_prefer_server_ciphers on;
    access_log  logs/www.zerounix.com_access.log access;
    error_log   logs/www.zerounix.com_error.log;

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

    location ~ .*\.(php|php5)$ {
        #fastcgi_pass 127.0.0.1:9000;
        fastcgi_pass   unix:/dev/shm/php-fpm.socket;
        include        fastcgi.conf;
        try_files $uri =404;
    }
}
```


## 通过第三方SSL签发机构签发SSL证书 ##

### 使用 OpenSSL 生成 SSL Key 和 CSR ###
由于只有浏览器或者系统信赖的 CA 才可以让所有的访问者通畅的访问你的加密网站，而不是出现证书错误的提示。所以我们跳过自签证书的步骤，直接开始签署第三方可信任的 SSL 证书吧。
OpenSSL 在 Linux、OS X 等常规的系统下默认都安装了，因为一些安全问题，一般现在的第三方 SSL 证书签发机构都要求起码 2048 位的 RSA 加密的私钥。同时，普通的 SSL 证书认证分两种形式，一种是 DV（Domain Validated），还有一种是 OV （Organization Validated），前者只需要验证域名，后者需要验证你的组织或公司，在安全性方面，肯定是后者要好。无论你用 DV 还是 OV 生成私钥，都需要填写一些基本信息，这里我们假设如下：
域名，也称为 Common Name，因为特殊的证书不一定是域名：example.com

* 组织或公司名字（Organization）：Example, Inc.
* 部门（Department）：可以不填写，这里我们写 Web Security
* 城市（City）：Beijing
* 省份（State / Province）：Beijing
* 国家（Country）：CN
* 加密强度：2048 位，如果你的机器性能强劲，也可以选择 4096 位

按照以上信息，使用 OpenSSL 生成 key 和 csr 的命令如下
```
openssl req -new -newkey rsa:2048 -sha256 -nodes -out example_com.csr -keyout example_com.key -subj "/C=CN/ST=Beijing/L=Beijing/O=Example Inc./OU=Web Security/CN=example.com"  
```

PS：如果是泛域名证书，则应该填写 `*.example.com`
你可以在系统的任何地方运行这个命令，会自动在当前目录生成 example_com.csr 和 example_com.key 这两个文件
接下来你可以查看一下 example_com.csr，得到类似这么一长串的文字
```
-----BEGIN CERTIFICATE REQUEST-----
MIICujCCAaICAQAwdTELMAkGA1UEBhMCQ04xEDAOBgNVBAgTB0JlaWppbmcxEDAO  
BgNVBAcTB0JlaWppbmcxFTATBgNVBAoTDEV4YW1wbGUgSW5jLjEVMBMGA1UECxMM  
V2ViIFNlY3VyaXR5MRQwEgYDVQQDEwtleGFtcGxlLmNvbTCCASIwDQYJKoZIhvcN  
AQEBBQADggEPADCCAQoCggEBAPME+nvVCdGN9VWn+vp7JkMoOdpOurYMPvclIbsI  
iD7mGN982Ocl22O9wCV/4tL6DpTcXfNX+eWd7CNEKT4i+JYGqllqP3/CojhkemiY  
SF3jwncvP6VoST/HsZeMyNB71XwYnxFCGqSyE3QjxmQ9ae38H2LIpCllfd1l7iVp  
AX4i2+HvGTHFzb0XnmMLzq4HyVuEIMoYwiZX8hq+kwEAhKpBdfawkOcIRkbOlFew  
SEjLyHY+nruXutmQx1d7lzZCxut5Sm5At9al0bf5FOaaJylTEwNEpFkP3L29GtoU  
qg1t9Q8WufIfK9vXqQqwg8J1muK7kksnbYcoPnNgPx36kZsCAwEAAaAAMA0GCSqG  
SIb3DQEBBQUAA4IBAQCHgIuhpcgrsNwDuW6731/DeVwq2x3ZRqRBuj9/M8oONQen  
1QIacBifEMr+Ma+C+wIpt3bHvtXEF8cCAJAR9sQ4Svy7M0w25DwrwaWIjxcf/J8U  
audL/029CkAuewFCdBILTRAAeDqxsAsUyiBIGTIT+uqi+EpGG4OlyKK/MF13FxDj  
/oKyrSJDtp1Xr9R7iqGCs/Zl5qWmDaLN7/qxBK6vX2R/HLhOK0aKi1ZQ4cZeP7Mr
8EzjDIAko87Nb/aIsFyKrt6Ze3jOF0/vnnpw7pMvhq+folWdTVXddjd9Dpr2x1nc  
y5hnop4k6kVRXDjQ4OTduQq4P+SzU4hb41GIQEz4  
-----END CERTIFICATE REQUEST-----
```
这个 CSR 文件就是你需要提交给 SSL 认证机构的，当你的域名或组织通过验证后，认证机构就会颁发给你一个 example_com.crt

而 example_com.key 是需要用在 Nginx 配置里和 example_com.crt 配合使用的，需要好好保管，千万别泄露给任何第三方

### Nginx 配置 HTTPS 网站以及增加安全的配置 ### 
你需要提交 CSR 文件给第三方 SSL 认证机构，通过认证后，他们会颁发给你一个 CRT 文件，我们命名为 example_com.crt
同时，为了统一，你可以把这三个文件都移动到 /etc/ssl/private/ 目录。
然后可以修改 Nginx 配置文件
```
server {  
    listen 80;
    listen [::]:80 ssl ipv6only=on; 
    listen 443 ssl;
    listen [::]:443 ssl ipv6only=on;
    server_name example.com;

    ssl on;
    ssl_certificate /etc/ssl/private/example_com.crt;
    ssl_certificate_key /etc/ssl/private/example_com.key;
}
```
检测配置文件没问题后重新读取 Nginx 即可
```
nginx -t && nginx -s reload
```
但是这么做并不安全，默认是 SHA-1 形式，而现在主流的方案应该都避免 SHA-1，为了确保更强的安全性，我们可以采取迪菲－赫尔曼密钥交换

首先，进入 /etc/ssl/certs 目录并生成一个 dhparam.pem
```
cd /etc/ssl/certs  
openssl dhparam -out dhparam.pem 2048 # 如果你的机器性能足够强大，可以用 4096 位加密  
```
生成完毕后，在 Nginx 的 SSL 配置后面加入
```
ssl_prefer_server_ciphers on;
ssl_dhparam /etc/ssl/certs/dhparam.pem;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS !RC4";
keepalive_timeout 70;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m; 
```
同时，如果是全站 HTTPS 并且不考虑 HTTP 的话，可以加入 HSTS 告诉你的浏览器本网站全站加密，并且强制用 HTTPS 访问
```
add_header Strict-Transport-Security max-age=63072000;
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
```
同时也可以单独开一个 Nginx 配置，把 HTTP 的访问请求都用 301 跳转到 HTTPS
```
server {  
        listen 80;
        listen [::]:80 ipv6only=on;
        server_name     example.com;
        return 301 https://example.com$request_uri;
}
```
### 可靠的第三方 SSL 签发机构 ###
众所周知，前段时间某 NIC 机构爆出过针对 Google 域名的证书签发的丑闻，所以可见选择一家靠谱的第三方 SSL 签发机构是多么的重要。

目前一般市面上针对中小站长和企业的 SSL 证书颁发机构有：

[StartSSL](https://www.startssl.com/)

[Comodo](https://www.comodo.com/) / 子品牌 [Positive SSL](https://www.positivessl.com/)

[GlobalSign](https://www.globalsign.com/en/) / 子品牌[AlphaSSL](https://www.alphassl.com/)

[GeoTrust](https://www.geotrust.com/) / 子品牌 [RapidSSL](https://www.rapidssl.com/)

其中 Postivie SSL、AlphaSSL、RapidSSL 等都是子品牌，一般都是三级四级证书，所以你会需要增加 CA 证书链到你的 CRT 文件里。

以 Comodo Positive SSL 为例，需要串联 CA 证书，假设你的域名是 example.com

那么，串联的命令是
```
cat example_com.crt COMODORSADomainValidationSecureServerCA.crt COMODORSAAddTrustCA.crt AddTrustExternalCARoot.crt > example_com.signed.crt  
```
在 Nginx 配置里使用 example_com.signed.crt 即可

如果是一般常见的 AplhaSSL 泛域名证书，他们是不会发给你 CA 证书链的，那么在你的 CRT 文件后面需要加入 AlphaSSL 的 CA 证书链

[AlphaSSL Intermediate CA](https://www.alphassl.com/support/install-root-certificate.html)
