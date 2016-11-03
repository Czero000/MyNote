
#### 查看当前版本信息

```
openssl version
OpenSSL 0.9.8e-fips-rhel5 01 Jul 2008
```


#### 安装新版本openssl

```
[root@Charlie ~]# wget http://www.openssl.org/source/openssl-1.0.1g.tar.gz -O /usr/local/src/openssl-1.0.1g.tar.gz
[root@Charlie ~]# cd /usr/local/src/
[root@Charlie src]# cd openssl-1.0.1g
[root@Charlie openssl-1.0.1g]# ./config shared zlib
[root@Charlie openssl-1.0.1g]# make && make install
[root@Charlie openssl-1.0.1g]# mv /usr/bin/openssl /usr/bin/openssl.bak
[root@Charlie openssl-1.0.1g]# mv /usr/include/openssl /usr/include/openssl.bak
[root@Charlie openssl-1.0.1g]# ln -s /usr/local/ssl/bin/openssl /usr/bin/openssl
[root@Charlie openssl-1.0.1g]# ln -s /usr/local/ssl/include/openssl /usr/include/openssl
```

#### 配置库文件搜索路径
```
[root@Charlie openssl-1.0.1g]# echo "/usr/local/ssl/lib" >> /etc/ld.so.conf
[root@Charlie openssl-1.0.1g]# ldconfig -v
```

#### 验证升级

```
[root@Charlie openssl-1.0.1g]# openssl version -a
OpenSSL 1.0.1g 7 Apr 2014
built on: Tue Apr 15 15:47:31 CST 2014
platform: linux-elf
options:  bn(64,32) rc4(8x,mmx) des(ptr,risc1,16,long) idea(int) blowfish(idx)
compiler: gcc -fPIC -DOPENSSL_PIC -DZLIB -DOPENSSL_THREADS -D_REENTRANT -DDSO_DLFCN -DHAVE_DLFCN_H -Wa,--noexecstack -DL_ENDIAN -DTERMIO -O3 -fomit-frame-pointer -Wall -DOPENSSL_BN_ASM_PART_WORDS -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DMD5_ASM -DRMD160_ASM -DAES_ASM -DVPAES_ASM -DWHIRLPOOL_ASM -DGHASH_ASM
OPENSSLDIR: "/usr/local/ssl"
```
 
在升级了openssl后，我们还要升级一下SSH
```
[root@Charlie openssl-1.0.1g]# ssh -V
OpenSSH_4.3p2, OpenSSL 0.9.8e-fips-rhel5 01 Jul 2008
```

#### 安装openssh
```
[root@Charlie src]# wget http://ftp.jaist.ac.jp/pub/OpenBSD/OpenSSH/portable/openssh-6.6p1.tar.gz
[root@Charlie src]# tar -zxf openssh-6.6p1.tar.gz
[root@Charlie src]# cd openssh-6.6p1
[root@Charlie openssh-6.6p1]# ./configure  --prefix=/usr --sysconfdir=/etc/ssh --with-zlib --with-pam  --with-ssl-dir=/usr/local/ssl --with-md5-passwords --mandir=/usr/share/man
[root@Charlie openssh-6.6p1]# make && make install 
[root@Charlie openssh-6.6p1]# ssh -V
OpenSSH_6.6p1, OpenSSL 1.0.1g 7 Apr 2014
```

#### TroubleShooting
报错：`configure: error: PAM headers not found`
解决：`yum install -y pam-devel`
