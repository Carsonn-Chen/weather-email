#! /usr/bin/python

import urllib.request
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

url = "http://www.weather.com.cn/weather/101010100.shtml"
header = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")  # 设置头部信息
opener = urllib.request.build_opener()  # 修改头部信息
opener.addheaders = [header]         # 修改头部信息
request = urllib.request.Request(url)   # 制作请求
response = urllib.request.urlopen(request)   # 得到请求的应答包
html = response.read()   # 将应答包里面的内容读取出来
html = html.decode('utf-8')    # 使用utf-8进行编码，不重新编码就会成乱码

find = []

bs = BeautifulSoup(html,'html.parser')
body = bs.body
data = body.find('div',{'id':'7d'})
ul = data.find('ul')
li = ul.find_all('li')


def get_cd_weather():
    weather_data = []
    for i in li:
        strs = ''
        date = i.find('h1').string
        strs += str(time.strftime('%Y', time.localtime(time.time()))) + '年' + str(time.strftime('%m', time.localtime(time.time()))) + '月' + date + '\t'
        weather = i.find('p').string
        strs += weather + '\t'
        max_c = i.find('span').string
        min_c = i.find('i').string
        if max_c == None:
            max_c = ''
        elif min_c == None:
            min_c = ''
        C = max_c + '\\' + min_c
        # print(date,weather,max_c,min_c)
        strs += C
        weather_data.append(strs)
    return weather_data


# 发送邮箱基本配置
smtpserver = 'smtp.qq.com'
user_name = 'carsonn@qq.com'
password = 'kkegwqqmbkgjbffj'
sender = 'carsonn@qq.com'

receiver = ['1102623875@qq.com']

# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息
subject = '专属每日天气预报详情 (●ω●) '
subject = Header(subject,'utf-8').encode()

# 构造邮件对象MIMEultipart对象
# 下面的主题、发件人、收件人、日期显示在邮件页面上
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = 'carsonn@qq.com <妍妍的帅气父亲(˙ω˙)>'
msg['To'] = ';'.join(receiver)
msg['Date'] = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))

weather = get_cd_weather()
html = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>天气预报</title>
</head>
<body>
<center>
<font size="5" font-family: "Arial","Microsoft YaHei","黑体","宋体",sans-serif;>北京一周的天气情况，请查收哦小家伙</font>
</center>
<table border="0" align="center">
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
  <tr>
    <td>%s</td>
  </tr>
</table>
</body>
</html>
'''% (weather[0], weather[1], weather[2], weather[3], weather[4], weather[5], weather[6])
text_html = MIMEText(html, 'html', 'utf-8')
msg.attach(text_html)

smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
smtp.login(user_name, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()