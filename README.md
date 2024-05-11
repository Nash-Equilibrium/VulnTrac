# ciscn
信安赛作品赛代码仓库



### 启动方法

1. 安装Redis，启动redis-server

2. 启动celery ，在另一个终端执行

	```shell
	$ celery -A app.celery worker --beat --scheduler redis --loglevel=info
	```

​	3.执行app.py ,flask服务器打开即可
