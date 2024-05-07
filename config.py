# Description: 配置文件
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:zyh20030827@localhost:3306/mydb"
SQLALCHEMY_TRACK_MODIFICATIONS = False
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
