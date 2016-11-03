Nginx默认不支持日志轮滚，通过下面方法解决

### 脚本方式
```
#!/bin/bash                                                                                                                         
log_dir='/usr/local/nginx/logs'                                                                                                     
nginx_pid='/usr/local/nginx/logs/nginx.pid'
date_yesterday=`date -d "yesterday" +%Y%m%d`
for logfile in `ls $log_dir/*.log | awk -F'/' '{print $6}'`                                                                         
do
        mv $log_dir/$logfile $log_dir/${logfile}_${date_yesterday}                                                                  
done
find $log_dir -ctime +15 | xargs rm -f
kill -USR1 `ps axu | grep "nginx: master process" | grep -v grep | awk '{print $2}'`
```

### 系统logrotate
```
cat /etc/logrotate.d/nginx
/usr/local/nginx/logs/*.log {
    daily
    missingok
    rotate 99
    compress
    delaycompress
    notifempty
    create 640 nobody nobody
    sharedscripts
    prerotate
    sleep 59
    endscript
    postrotate
        if [ -f /usr/local/nginx/logs/nginx.pid ]; then
                kill -USR1 `cat /usr/local/nginx/logs/nginx.pid`
        fi
    endscript
}
```
