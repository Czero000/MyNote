通过curl的-w参数我们可以自定义curl的输出，`%{http_code}`代表http状态码
```
curl -I -m 10 -o /dev/null -s -w %{http_code}  www.letuknowit.com
```
上面的输出是不含换行的，如果需要换行的话，加上`\n`
```
curl -I -m 10 -o /dev/null -s -w %{http_code}  www.letuknowit.com
200# curl -I -m 10 -o /dev/null -s -w %{http_code}"\n"  www.letuknowit.com
200
```
