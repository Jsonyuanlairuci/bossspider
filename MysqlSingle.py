from functools import wraps
import mysql.connector

# 单例模式实现数据库连接
def singleton(cls):
    instance={}

    @wraps(cls)
    def get_instance(*args,**kw):
        if cls not in instance:
            instance[cls]=cls(*args,**kw)
        return instance[cls]

    return get_instance   


# 数据库连接实例
@singleton
class MYSQLSingel(object):
    def __init__(self,conn='',cursor='') -> None:
        self.conn=conn
        self.cursor=cursor


    def get_conn(self,host='127.0.0.1',user='root',password='root',database='boss'):
        try:
            self.conn=mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            ) 
            
        except Exception as e:
            print('File to connect database:%s' %e)
        self.cursor=self.conn.cursor(buffered=True)
        return self.cursor , self.conn



 




