import MysqlSingle
import sys
import threading
import time
import queue
import mysql

class ToMysql():
    def __init__(self,fileName='php') -> None:
        self.fileName=fileName
        pass

    def getData(self):
        with open(sys.path[0]+'\\data\\{}.txt'.format(self.fileName),'r',encoding='utf-8') as f:
            data=f.readlines()
            for index in range(len(data)):
                yield eval(data[index])         #字符串转换为字典

        pass

    # 处理数据为元组的形式，方便直接插入数据库
    def getTuple(self,row,mysqlQueue:queue.Queue):
        salaryList=row['salary_range'].split('·')
        otherSalary=salaryList[1] if len(salaryList)>1 else ''
        salaryBegin=salaryList[0].replace('K','').split('-')
        experienceList=row['experience'].replace('年','').split('-')
        experienceEnd=experienceList[1] if len(experienceList)>1 else ''
        companyInfoList=row['company_info'].split('/')
        numberRangeList=companyInfoList[-2].replace('人','').split('-')
        numrangeEnd=numberRangeList[1] if len(numberRangeList)>1 else ''
        val=(
            row['work_name'],
            self.fileName,
            salaryBegin[0],
            salaryBegin[1],
            otherSalary,
            experienceList[0],
            experienceEnd,
            row['education'],
            row['tech_stack'].replace('///',''),
            row['company'],
            row['company_info'],
            numberRangeList[0],
            numrangeEnd,
            int(time.time())
            )
        # print(val)
        mysqlQueue.put(val)

    # 通过消息队列获取数据并且插入到数据库中
    def insertData(self,mysqlQueue:queue.Queue,mysqlConnCursor):
     
        while True:
            result=mysqlQueue.get()
            sql=" \
            insert into workes \
            ( \
                `title`, \
                `programming_language`, \
                `salary_begin`, \
                `salary_end`, \
                `other_salary`, \
                `experience_begin`, \
                `experience_end`, \
                `education`, \
                `tech_stack`, \
                `company` , \
                `company_info`, \
                `number_range_begin`, \
                `number_range_end`, \
                `create_time`, \
            )  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            try:
                mysqlConnCursor.execute(sql,result)
                mysqlConnCursor.commit()
                print("1 条记录已插入, ID:", mysqlConnCursor.lastrowid())
                pass
            except BaseException as e:
                print(e)
                pass
        pass    

    # 多线程 + 队列的形式处理数据，切插入数据库
    def run(self):
        mysql=MysqlSingle.MYSQLSingel()
        mysqlConnCursor,conn=mysql.get_conn()
        data=self.getData()
        mysqlQueue=queue.Queue()
        for row in data:
            t=threading.Thread(target=self.getTuple,args=(row,mysqlQueue,))   #使用多线程的方式处理数据      队列生产者生产数据
            t.start()
            pass
        
        for index in range(5):
            t=threading.Thread(target=self.insertData,args=(mysqlQueue,mysqlConnCursor,))      #消费者  消费队列
            t.start()

        mysqlConnCursor.close()
        conn.close()    

        
            


toMysql=ToMysql('php')
toMysql.run()        