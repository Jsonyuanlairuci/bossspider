from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from Response import getDrivertDriverByWebdriver
import sys

class BossSpider():
    def __init__(self,url,mobile='',workName='') -> None:
        self.mobile=mobile
        self.workName=workName
        self.driver=getDrivertDriverByWebdriver(url)
        self.f=open(sys.path[0]+'\\data\\{}.txt'.format(self.workName),'w+',encoding='utf-8')
        pass

    def loginBoss(self):
        # 进入主页，点击登录
        driver=self.driver
        time.sleep(random.randint(2,5))
        loginButton=driver.find_element(By.XPATH,'//*[@id="header"]/div[1]/div[4]/div/a[4]')
        time.sleep(1)
        loginButton.click()
        time.sleep(random.randint(3,7))
        # 获取登陆手机号输入框
        mobileInput=driver.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/span[2]/input')
        # 输入手机号
        mobileInput.send_keys(self.mobile)
        time.sleep(random.randint(2,5))
        verifyCodeButton=driver.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span/div/span')
        time.sleep(random.randint(2,5))
        # 点击获取验证码
        verifyCodeButton.click()
        time.sleep(random.randint(4,7))
        code=input('请输入验证码：')
        if len(code)>0:
            # 输入验证码并且登录
            codeInput=driver.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/span/input')
            codeInput.send_keys(code)
            time.sleep(1)
            # 同意协议
            agreementButton=driver.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[2]/span/input')
            agreementButton.click()
            # 点击登录
            loginButton=driver.find_element(By.XPATH,'//*[@id="wrap"]/div/div[2]/div[2]/div[2]/div[1]/div[3]/button')
            loginButton.click()
            self.searchWork()
        pass
    
    
    def searchWork(self):
        time.sleep(random.randint(6,9))
        searchInput=WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="search-input-box"]/div[@class="input-wrap input-wrap-text"]/input'))
        )
        searchInput.send_keys(self.workName)
        time.sleep(random.randint(5,8))
        searchButton=self.driver.find_element(By.XPATH,'//a[@class="search-btn"]')
        time.sleep(random.randint(5,9))
        searchButton.click()
        time.sleep(random.randint(7,10))
        self.getList()
        pass

    def getList(self):
       
        driver=self.driver
        index=1
        while index<11:
            time.sleep(random.randint(10,15))
            lis=WebDriverWait(driver=driver,timeout=100).until(
                EC.presence_of_all_elements_located((By.XPATH,'//*[@id="wrap"]//ul[@class="job-list-box"]/li'))
            )
            
            for li in lis:
                workNameStr=li.find_element(By.XPATH,'.//span[@class="job-name"]').text
                positionStr=li.find_element(By.XPATH,'.//span[@class="job-area"]').text
                salaryRangeStr=li.find_element(By.XPATH,'.//span[@class="salary"]').text
                experienceRangeStr=li.find_element(By.XPATH,'.//ul[@class="tag-list"]/li[1]').text
                educationStr=li.find_element(By.XPATH,'.//div[@class="job-info clearfix"]/ul/li[2]').text
                companyNameStr=li.find_element(By.XPATH,'.//h3[@class="company-name"]/a').text
                # peopleNumRangeStr=li.find_element(By.XPATH,'.//div[1]/div/div[2]/ul/li[3]').text
                techStackEles=li.find_elements(By.XPATH,'.//div[@class="job-card-footer clearfix"]/ul/li')
                techStackStr=''
                for index in range(len(techStackEles)):
                    techStackStr+=techStackEles[index].text+'/'

                companyInfoList=li.find_elements(By.XPATH,'.//div[@class="company-info"]/ul[@class="company-tag-list"]/li')
                companyInfoStr=''
                for index in range(len(companyInfoList)):
                    companyInfoStr+=companyInfoList[index].text+'/'

                val={
                    'work_name':workNameStr,
                    'position':positionStr,
                    'salary_range':salaryRangeStr,
                    'experience':experienceRangeStr,
                    'education':educationStr,
                    'tech_stack':techStackStr,
                    'company':companyNameStr,
                    'company_info':companyInfoStr
                    }
                print(val)
                self.f.write(repr(val)+'\n')
                yield val
            time.sleep(random.randint(10,15))    
            js="var q=document.documentElement.scrollTop=100000"      
            driver.execute_script(js)
            time.sleep(random.randint(3,5))
            nextPage=driver.find_element(By.XPATH,'//div[@class="options-pages"]/a[10]')    
            nextPage.click()
            # time.sleep(random.randint(2.4))
            # # 翻页后刷新页面
            # driver.refresh()
            index+=1
        pass


    def run(self):
        result=self.loginBoss()
        for row in result:
            print(row)
        self.f.close()
        pass


def main():
    # url="https://www.zhipin.com/web/geek/job?query=php&city=101270100"
    # workName='php'
    # bossSpider=BossSpider(url=url,workName=workName)
    # bossSpider.run()
    mobile=input('请输入手机号：')
    workName='php'
    if len(mobile)>0:
       url="https://www.zhipin.com/chengdu"
       bossSpider=BossSpider(url,mobile,workName)
       bossSpider.run() 
    


if __name__=="__main__":
    main()


   