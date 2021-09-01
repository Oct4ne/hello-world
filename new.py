# coding=utf-8
from PIL import Image
import time
from selenium import  webdriver
import requests
import json

driver = webdriver.Edge(r'D:\pythonProject\Scripts\msedgedriver.exe')
driver.maximize_window()
driver.get('http://10.33.20.100/ydata/login.do')


#清空登录框
driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/input").clear()
#输入用户名
driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/input").send_keys("330500fxz")
#清空密码
driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/input").clear()
#输入密码
driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/input").send_keys("Qwaszx1234")
#清除验证码
driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/input").clear()
#识别验证码
element = driver.find_element_by_xpath('/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[5]/td[2]/img[2]')
element.screenshot('code.png')
#输入验证码

import sys
import json
import base64


# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
else:
    from urllib import urlencode

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'CMYbudLQO1rwkqMqG4rZb9Hu'

SECRET_KEY = 'bTbeuUlzuBvQblZlyciZ9ZCYioxWswiM'


OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

if __name__ == '__main__':

    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    text = ""

    # 读取书籍页面图片
    file_content = read_file('./code.png')

    # 调用文字识别服务
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

    # 解析返回结果
    result_json = json.loads(result)
    for words_result in result_json["words_result"]:
        text = text + words_result["words"]


    # 打印文字
    print(text)



driver.find_element_by_xpath("/html/body/form/table[2]/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/input").send_keys(text.strip())
#点击登录按钮
driver.find_element_by_xpath("/html/body/map/area[1]").click()
#获取cookie
cookie = driver.get_cookies()
print(cookie)
jsoncookies = json.dumps(cookie)
with open("homepage.json",'w') as f:
    f.write(jsoncookies)
str = ''
with open('homepage.json','r',encoding='utf-8') as f:
    listcookies = json.loads(f.read())
cookie = [item["name"] + "=" + item["value"] for item in listcookies]
cookiestr = '; '.join(item for item in cookie)
print(cookiestr)

dataurl = "http://10.33.20.100/ydata/surveyobject/forwardtobasedata.do?code=8600000002020102907400790"

headers = {
    'cookie':cookiestr,
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'
}

html = requests.get(url=dataurl,headers=headers)

print(html.text)



