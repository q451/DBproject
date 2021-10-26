from django.shortcuts import render, redirect
from .models import test, movie
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request,urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import pymysql

findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，标售规则   影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

# Create your views here.
def create(request):
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    # 创建数据库表
    cursor.execute("DROP TABLE IF EXISTS function_app_movie")
    sql = '''
                create table function_app_movie(
                id integer  primary key auto_increment,
                url_link text,
                photo_link text,
                chinese_name char(100),
                origin_name char(100) ,
                score double,
                rated numeric,
                introduction text,
                actors text)
                '''
    print(sql)
    cursor.execute(sql)
    print('创建成功')

def count_show(request):
    r_count = movie.objects.all().count()
    movies = movie.objects.all()
    context = {
        'r_count': r_count,
        'movies': movies
    }
    return render(request, 'function/test.html', context)

def dou_ban(request):
    movies = movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'function/movie.html', context)

def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def getData():
    baseurl = "https://movie.douban.com/top250?start="  # 要爬取的网页链接
    data_list = []  # 用来存储爬取的网页信息
    for i in range(0, 10):  # 调用获取页面信息的函数，10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # print(html)
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串
            data = []  # 保存一部电影所有信息
            item = str(item)
            link = re.findall(findLink, item)[0]  # 通过正则表达式查找
            data.append(link)
            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle, item)
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 消除转义字符
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')
            rating = re.findall(findRating, item)[0]
            data.append(rating)
            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
            bd = re.sub('/', "", bd)
            data.append(bd.strip())
            data_list.append(data)
    for data in data_list:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
        cursor = db.cursor()
        sql = '''
            insert into function_app_movie(
            url_link,photo_link,chinese_name,origin_name,score,rated,introduction,actors)
            values (%s)''' % ",".join(data)
        cursor.execute(sql)
        db.commit()
    print('爬取数据成功')
    db.close()
