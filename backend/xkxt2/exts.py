#解耦防止循环引用
import pymysql
import threading

mutex=threading.Lock()

# db = pymysql.connect("localhost", "root", "zyh19980310", "xkxt",use_unicode=True,charset='utf8')

db = pymysql.connect("106.14.140.30", "Ubuntu", "123456", "db2",port=3306,use_unicode=True,charset='utf8'
,connect_timeout =31536000)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


def start_job():
    global db
    try:
        db.ping()
    except:
        db = pymysql.connect("106.14.140.30", "Ubuntu", "123456", "db2", port=3306, use_unicode=True, charset='utf8',connect_timeout =31536000)


