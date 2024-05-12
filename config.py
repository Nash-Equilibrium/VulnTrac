# Description: 配置文件

# Flask-SQLAlchemy数据库连接URI
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zyh20030827@localhost:3306/mydb"
# 不再跟踪对象的修改并发送信号
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Celery消息代理(Message Broker)的连接URL
CELERY_BROKER_URL = "redis://localhost:6379/0"
# Celery任务结果存储的连接URL
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
