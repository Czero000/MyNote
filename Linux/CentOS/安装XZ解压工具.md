从www.kernel.org下载内核安装包，准备CentOS6.5内核升级到3.x，下载后发现是一个以.xz结尾的压缩包。
>xz 是一个使用 LZMA压缩算法的无损数据压缩文件格式。 和gzip与bzip2一样，同样支持多文件压缩，但是约定不能将多于一个的目标文件压缩进同一个档案文件。 相反，xz通常作为一种归档文件自身的压缩格式，例如使用tar或cpioUnix程序创建的归档。 xz 在GNU coreutils（版本 7.1 或更新）[1]中被使用。 xz 作为压缩软件包被收录在 Fedora (自Fedora 12起)[2], Arch Linux[3], FreeBSD、 Slackware Linux、CRUX和 Funtoo Linux中。
xz 以其优异的性能和压缩比[4]成为了不少开源软件（例如 Linux 内核源码、Debian deb[5] 和 Fedora rpm）的压缩方式之一，甚至是默认压缩方式。xz 命令行程序曾有过一个名为 pxz 的分支，提供多线程压缩功能，后来 xz 在 5.2 时本身就直接提供多线程了.

[XZ Utils官方网站](http://tukaani.org/xz/)

#### 下载软件包
```
wget http://tukaani.org/xz/xz-5.2.2.tar.gz
```

#### 解压
```
tar -zxf xz-5.2.2.tar.gz 
```

### 编译安装
```
./configure  
make && make install 
```

### 使用方法
```
 xz --help
Usage: xz [OPTION]... [FILE]...
Compress or decompress FILEs in the .xz format.

  -z, --compress      force compression
  -d, --decompress    force decompression
  -t, --test          test compressed file integrity
  -l, --list          list information about .xz files
  -k, --keep          keep (don't delete) input files
  -f, --force         force overwrite of output file and (de)compress links
  -c, --stdout        write to standard output and don't delete input files
  -0 ... -9           compression preset; default is 6; take compressor *and*
                      decompressor memory usage into account before using 7-9!
  -e, --extreme       try to improve compression ratio by using more CPU time;
                      does not affect decompressor memory requirements
  -T, --threads=NUM   use at most NUM threads; the default is 1; set to 0
                      to use as many threads as there are processor cores
  -q, --quiet         suppress warnings; specify twice to suppress errors too
  -v, --verbose       be verbose; specify twice for even more verbose
  -h, --help          display this short help and exit
  -H, --long-help     display the long help (lists also the advanced options)
  -V, --version       display the version number and exit

With no FILE, or when FILE is -, read standard input.

Report bugs to  (in English or Finnish).
XZ Utils home page: 
```
```
解压： xz -d linux-3.12.50.tar.xz 
压缩： xz -z linux-3.12.50.tar 
```
