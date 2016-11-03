```
groupadd mysql 
useradd -s /usr/sbin/nologin -g mysql -M mysql
tar -zxf mariadb-10.1.14.tar.gz
cd mariadb-10.1.14
cmake \
-DCMAKE_INSTALL_PREFIX=/usr/local/mysql \
-DMYSQL_DATADIR=/usr/local/mysql/data \
-DMYSQL_UNIX_ADDR=/tmp/mysql.sock \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_EXTRA_CHARSETS=all \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_ARCHIVE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
-DWITH_PARTITION_STORAGE_ENGINE=1\
-DWITH_READLINE=1 \
-DWITH_EMBEDDED_SERVER=1 \  
-DENABLED_LOCAL_INFILE=1 \
-DWITH_SSL=system

cd /usr/local/mysql
cp support-files/mysql.server /etc/init.d/mysql
chmod +x /etc/init.d/mysql     
cp support-files/my-medium.cnf /etc/my.cnf
chown -R mysql data
chgrp -R mysql .
scripts/mysql_install_db --user=mysql
/usr/local/mysql/bin/mysqld_safe  --user=mysql &
bin/mysqladmin  -u root password '8ql6,yhY'
/usr/local/mysql/bin/mysql -uroot -p
```
