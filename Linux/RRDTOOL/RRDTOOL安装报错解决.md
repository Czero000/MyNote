在安装rrdtool过程中，出现报错，原来是缺少perl模块
### 报错信息
```


Can't locate ExtUtils/MakeMaker.pm in @INC (@INC contains: /usr/local/lib64/perl5 /usr/local/share/perl5 /usr/lib64/perl5/vendor_perl /usr/share/perl5/vendor_perl /usr/lib64/perl5 /usr/share/perl5 .) at Makefile.PL line 1.

BEGIN failed--compilation aborted at Makefile.PL line 1.

make[3]: *** [perl-piped/Makefile] Error 2

make[3]: Leaving directory `/usr/local/src/rrdtool-1.4.9/bindings'

make[2]: *** [all-recursive] Error 1

make[2]: Leaving directory `/usr/local/src/rrdtool-1.4.9/bindings'

make[1]: *** [all-recursive] Error 1

make[1]: Leaving directory `/usr/local/src/rrdtool-1.4.9'

make: *** [all] Error 2
```
### 解决方法
```
yum install perl-ExtUtils-CBuilder perl-ExtUtils-MakeMaker

```
