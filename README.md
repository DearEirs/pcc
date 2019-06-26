# pcc

demo for pcc

## 接口测试
http://0.0.0.0:8000/pcc?action=like&oid=8000100038&uid=6000100345

http://0.0.0.0:8000/pcc?action=is_like&oid=8000100038&uid=6000100345

http://0.0.0.0:8000/pcc?action=count&oid=8000100038

http://0.0.0.0:8000/pcc?action=list&uid=6000100010&oid=8000100037&cursor=0&page_size=100&is_friend=1

http://0.0.0.0:8000/pcc?action=list&uid=6000100010&oid=8000100037&cursor=0&page_size=100&is_friend=0

## 压测命令
./wrk -c 20 -t 10 -d 5 "http://0.0.0.0:8000/pcc?action=like&oid=8000100038&uid=6000100345"

./wrk -c 20 -t 10 -d 5 "http://0.0.0.0:8000/pcc?action=is_like&oid=8000100038&uid=6000100345"

./wrk -c 20 -t 10 -d 5 "http://0.0.0.0:8000/pcc?action=count&oid=8000100038"

./wrk -c 20 -t 10 -d 5 "http://0.0.0.0:8000/pcc?action=list&uid=6000100010&oid=8000100037&cursor=0&page_size=100&is_friend=1"

./wrk -c 20 -t 10 -d 5 "http://0.0.0.0:8000/pcc?action=list&uid=6000100010&oid=8000100037&cursor=0&page_size=100&is_friend=0"
