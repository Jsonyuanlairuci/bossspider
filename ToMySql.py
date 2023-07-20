import MysqlSingle
import sys
import threading
import time
import queue
import mysql.connector

class ToMysql():
    def __init__(self,fileName='php') -> None:
        self.fileName=fileName
        pass

    def getData(self):
        workData=[]
        with open(sys.path[0]+'\\data\\{}.txt'.format(self.fileName),'r',encoding='utf-8') as f:
            data=f.readlines()
            for index in range(len(data)):
                workData.append(data[index])          #字符串转换为字典

        return workData

    # 处理数据为元组的形式，方便直接插入数据库
    def getTuple(self,row):
        row=eval(row)
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
        return val
    # 通过消息队列获取数据并且插入到数据库中
    def insertData(self,data):
            Db=mysql.connector.connect(
                    host='127.0.0.1',
                    user='root',
                    passwd='root',
                    database='boss'
                )
            mysqlConnCursor=Db.cursor()
            insertData=[]
            # 数据库去重
            for index in range(len(data)):
                 selectSql="select id from workes where company='{}';".format(data[index][9])
                 mysqlConnCursor.execute(selectSql)
                 result=mysqlConnCursor.fetchall()            
                 if(len(result)<=0):
                      insertData.append(data[index])  
            # 列表去重
            oneData=[]
            for row in insertData:
                 if row not in oneData:
                      oneData.append(row)        
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
                `create_time` \
            )  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                mysqlConnCursor.executemany(sql,oneData)
                print("1 条记录已插入, ID:{}".format(mysqlConnCursor.lastrowid()) )
                pass
            except BaseException as e:
                print(e)
                pass
            finally:
                mysqlConnCursor.close()
                Db.close()  

    # 多线程 + 队列的形式处理数据，切插入数据库
    def run(self):
        data=self.getData()
        workData=[]
        for index in range(len(data)):
              workData.append(self.getTuple(row=data[index]))
        
        self.insertData(workData)

        
            


toMysql=ToMysql('php')
toMysql.run()        