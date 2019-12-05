
# @author：从北相北
# @弹幕点歌机
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import threading
import time
from bs4 import BeautifulSoup
import requests,json,re


class loginBili():

    def __init__(self):
        self.url = 'https://www.bilibili.com/'
        self.curl = 'https://passport.bilibili.com/login'  # B站登录界面
        self.uroom = "https://live.bilibili.com/" + roomid
        self.umsg = 'https://api.live.bilibili.com/msg/send'
        self.browser = webdriver.Chrome()
        self.browseropt = webdriver.ChromeOptions()
        # 定义显示等待
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWARD

    def __del__(self):
        # 关闭浏览器
        self.browser.close()

    def get_login_btn(self,btn):
        """
        登陆
        :return: None
        """
        '''
        <a class="btn btn-login">登录</a>
        值有空格的 查找时写一半就好 要么前半段要么后半段
        '''

        # button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-login')))
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, btn)))
        return button

    def open(self,url):

        """
        打开登陆界面，输入用户名和密码
        :return: None
        """
        self.browser.get(url)  # 打开网址
        # 找到用户名输入框
        # 在浏览器中定位它的HTML代码后 根据id属性来找
        '''
        <input type="text" value="" placeholder="你的手机号/邮箱" id="login-username" maxlength="50" autocomplete="off" class="">
        '''
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        # 找到密码输入框
        '''
        <input type="password" placeholder="密码" id="login-passwd" class="">
        '''
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))

        # 输入用户名和密码
        username.send_keys(self.username)
        password.send_keys(self.password)


    def login_start(self):
        """
        判断是否登陆成功
        :return:
        """
        try:
            self.open(self.curl)
            button = self.get_login_btn('btn')  # 找到登录按钮
            button.click()  # 点击
            # print(self.cookie)
            '''
           <a data-v-4d9bc88b="" href="//message.bilibili.com" target="_blank" title="消息" class="t"><div data-v-4d9bc88b="" class="num">3</div> <!---->
    消息
  </a>
            '''
            # 登录成功后 界面上会有一个消息按钮

            if(self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'signin')))):
                print('登陆成功')
            # self.getlive(chatmsg)
            return True


        except TimeoutException:
            print("登陆失败")
            return False

    def sendmsg(self,msg):
        if len(msg):
            self.getlive(msg.pop(0))
        else:
            exit()
        t = threading.Timer(120, self.sendmsg,[msg])
        t.start()

    def getlive(self,chatmsg):
        self.browseropt.add_argument('--headless')
        self.browser.get(self.uroom)
        # self.browser.find_element_by_class_name()
        chat = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chat-input')))
        chatmsg = "#点歌" + " " + chatmsg
        print(chatmsg)
        chat.send_keys(chatmsg)
        time.sleep(1)
        button = self.get_login_btn('bl-button')  # 找到登录按钮
        button.click()

    def getmusic(self,musiclist):
        musicurl = 'https://music.163.com/m/playlist?id=' + musiclist
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
                    Chrome/69.0.3497.100 Safari/537.36',
        }
        mus = []
        r = requests.get(musicurl, headers=headers)
        html = r.text.encode(r.encoding).decode()
        soup = BeautifulSoup(html, "lxml")
        res = soup.find_all("ul")[0]
        a = r'>*<li>'
        for rr in res:
            mus.append(rr.string)
        return mus


def sendmsg(msg):
    if len(msg):
        login.getlive(msg.pop(0))
    else:
        exit()
    t = threading.Timer(300, sendmsg,[msg])
    t.start()

if __name__ == '__main__':
    dm = []
    USERNAME = input("账号：\n")
    PASSWARD = input("密码：\n")
    roomid = input("直播间id：\n") #21574137
    musiclist = input("歌单id：\n") #412634380
    login = loginBili()
    msg = login.getmusic(musiclist)
    try:
        if login.login_start():
            sendmsg(msg)
    except:
        raise
