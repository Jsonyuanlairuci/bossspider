from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from my_fake_useragent import UserAgent
import requests


# 通过webdriver获取页面内容

def getDrivertDriverByWebdriver(url):
    opt=webdriver.ChromeOptions()
    # 请求头伪装
    opt.add_argument('--user-agent=%s' % UserAgent().random())
    # 已开发者模式启动浏览器
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
     # 屏蔽保存密码提示框
    prefs={'credentials_enable_service':False,'profile.password_manager_enabled':False}
    opt.add_experimental_option('prefs',prefs)
    # 反爬虫特征处理
    opt.add_argument('--disable-blink-features=AutomationControlled')
     #ip代理
    # opt.add_argument('--proxy-server={}'.format(getReuestIpProxies()))  
    driver=webdriver.Chrome(options=opt)
    # 浏览器最大化
    driver.maximize_window()
    driver.get(url=url)
    WebDriverWait(driver=driver,timeout=25)
    
    return driver


# 通过requests库获取页面内容
def getHtmlContentByRequests(url):
    # proxies={
    #     'http':'http://'+getReuestIpProxies()
    # }
    header={
        'User-Agent':UserAgent().random
    }
    reponse=requests.get(url=url,headers=header)
    reponse.encoding='utf-8'
    content=reponse.text
    return content








