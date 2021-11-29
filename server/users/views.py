from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import user_account, up_user
from function_app.models import test, movie
from .forms import RegisterForm, LoginForm, addForm
from django.contrib.auth import authenticate, login, logout
import hashlib
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import pymysql
from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings    # setting.py添加的的配置信息
import datetime

# Create your views here.

findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，标售规则   影片详情链接的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)

#@login_required(login_url='login_page')  # 强制登录才能显示
def error_dispose(request):
    message = ''
    results = ''
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    try:
        sql = '''
                SELECT * FROM function_app_movie order by id limit 0,1;
                '''
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        print(e)
    finally:
        message = "执行结束"
        db.close()
    print(message)
    context = {
        'message': message,
        'results': results,
        # 'error_type': e,
    }
    return render(request, 'error_page.html', context)
def base_page(request):
    message = ''
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    # try:
    sql = '''
            SELECT * FROM function_app_movie order by id limit 0,1;
            '''
    # except Exception as e:
    #     message = e
    # finally:
    message = "执行结束"
    db.close()

    cursor.execute(sql)
    results = cursor.fetchall()
    print(message)
    print(results)
    context = {
        'message': message,
        'results': results,
    }
    return render(request, 'base.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def index_page(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    movies = movie.objects.all()
    # counter = 0
    # top_250 = []
    # for i in movies:
    #     if counter<250:
    #         top_250.append(i)
    #         counter += 1
    #     else:
    #         break
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    sql = '''
        SELECT * FROM function_app_movie order by id limit 0,250;
        '''
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    paginator = Paginator(movies, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context = {
        'name': value_name,
        'id': value_id,
        'movies': movies,
        'contacts': contacts,
    }
    return render(request, 'index.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def evaluate(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    movies = movie.objects.all()

    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    sql = '''
        SELECT * FROM function_app_movie order by rated DESC limit 0,10;
        '''
    cursor.execute(sql)
    #获取所有游标
    results = cursor.fetchall()
    db.close()

    context = {
        'name': value_name,
        'id': value_id,
        'movies': movies,
        'results': results,
    }
    return render(request, 'max_critical.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def ping_top(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    cursor_Am = db.cursor()
    cursor_Rb = db.cursor()
    # sql = '''
    #     SELECT * FROM function_app_movie order by score DESC limit 0,20;
    #     '''
    sql = '''
            SELECT * FROM function_app_movie WHERE actors LIKE '_%%中国%%_' order by score DESC,rated DESC limit 0,5;
        '''
    sql1 = '''
             SELECT * FROM function_app_movie WHERE actors LIKE '_%%美国%%_' order by score DESC,rated DESC limit 0,5;
        '''
    sql2 = '''
            SELECT * FROM function_app_movie WHERE actors LIKE '_%%日本%%_' order by score DESC,rated DESC limit 0,5;
        '''
    cursor.execute(sql)
    cursor_Am.execute(sql1)
    cursor_Rb.execute(sql2)
    #获取所有游标
    results = cursor.fetchall()
    results1 = cursor_Am.fetchall()
    results2 = cursor_Rb.fetchall()
    db.close()
    context = {
        'name': value_name,
        'id': value_id,
        'Zh': results,
        'Am': results1,
        'Rb': results2,
    }
    return render(request, 'ping_feng.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def analysising(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    counts = movie.objects.all().count()
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    cursor_c = db.cursor()
    cursor_r= db.cursor()
    cursor_y = db.cursor()
    cursor_class1 = db.cursor()
    cursor_class2 = db.cursor()
    cursor_class3 = db.cursor()
    cursor_class4 = db.cursor()
    cursor_class5 = db.cursor()
    sql = '''
        SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%美国%%_' 
    '''
    sql_c = '''
        SELECT COUNT(actors) FROM function_app_movie WHERE actors LIKE '_%%中国%%_' 
    '''
    sql_r = '''
        SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%日本%%_' 
    '''
    sql_y = '''
        SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%印度%%_' 
    '''
    sql_cla1 = '''
        SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%爱情%%_' 
    '''
    sql_cla2 = '''
         SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%犯罪%%_' 
    '''
    sql_cla3 = '''
         SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%动画%%_' 
    '''
    sql_cla4 = '''
        SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%喜剧%%_' 
    '''
    sql_cla5 = '''
        SELECT COUNT(*) FROM function_app_movie WHERE actors LIKE '_%%历史%%_' 
    '''
    #国家拍摄数量
    cursor.execute(sql)
    cursor_c.execute(sql_c)
    cursor_y.execute(sql_y)
    cursor_r.execute(sql_r)
    #电影种类
    cursor_class1.execute(sql_cla1)
    cursor_class2.execute(sql_cla2)
    cursor_class3.execute(sql_cla3)
    cursor_class4.execute(sql_cla4)
    cursor_class5.execute(sql_cla5)
    #获取国家数量所有游标
    American = cursor.fetchall()
    China = cursor_c.fetchall()
    Japan = cursor_r.fetchall()
    YinDu = cursor_y.fetchall()
    #获取电影种类数量
    love = cursor_class1.fetchall()
    crime = cursor_class2.fetchall()
    cartoon = cursor_class3.fetchall()
    comedy = cursor_class4.fetchall()
    history = cursor_class5.fetchall()
    #国家数量转换
    x = China[0]
    x2 = American[0]
    x3 = Japan[0]
    x4 = YinDu[0]
    z1 = x[0]
    z2 = x2[0]
    z3 = x3[0]
    z4 = x4[0]
    y = list(x)
    y2 = list(x2)
    y3 = list(x3)
    y4= list(x4)
    counts = counts-z1-z2-z3-z4
    #电影种类转换
    a1 = love[0]
    a2 = crime[0]
    a3 = cartoon[0]
    a4 = comedy[0]
    a5 = history[0]
    b1 = a1[0]
    b2 = a2[0]
    b3 = a3[0]
    b4 = a4[0]
    b5 = a5[0]
    c1 = list(a1)
    c2 = list(a2)
    c3 = list(a3)
    c4 = list(a4)
    c5 = list(a5)
    #关闭数据库
    db.close()

    context = {
        'name': value_name,
        'id': value_id,
        'American': y2,
        'China': y,
        'Japan': y3,
        'YinDu': y4,
        'z1': z1,
        'z2': z2,
        'z3': z3,
        'z4': z4,
        'other': counts,
        'b1': b1,
        'b2': b2,
        'b3': b3,
        'b4': b4,
        'b5': b5,
        'c1': c1,
        'c2': c2,
        'c3': c3,
        'c4': c4,
        'c5': c5,
    }
    return render(request, 'analysis_page.html', context)

def welcome_page(request):
    return render(request, 'welcome.html')

def register_page(request):
    register_form = RegisterForm()
    message = ''
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            name = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password1 = register_form.cleaned_data['password1']
            phone = register_form.cleaned_data['phone']
            email = register_form.cleaned_data['email']

            users = user_account.objects.filter(username=name)
            phone1 = user_account.objects.filter(phone=phone)
            email1 = user_account.objects.filter(email=email)
            m = hashlib.md5()
            m.update(password.encode())
            password_m = m.hexdigest()

            if users:
                message = '该用户名已存在'
            elif phone1:
                message = '该手机号已存在'
            elif email1:
                message = '该邮箱已存在'
            elif password1 != password:
                message = '两次输入密码不一致'
            else:
                user = user_account.objects.create(username=name, password=password_m, phone=phone, email=email)
                user.save()
                return redirect('login_page')
    context = {  # 把后端数据传到前端页面显示
        'register_form': register_form,
        'message': message,
    }

    return render(request, 'register_page.html', context)

def login_page(request):
    message = ''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if 'btn1' in request.POST:
            if login_form.is_valid():
                # username = login_form.cleaned_data['username']
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                # 数据库密码加密验证
                m = hashlib.md5()
                m.update(password.encode())
                password_m = m.hexdigest()
                try:
                    # user = user_account.objects.get(username=username)
                    user = user_account.objects.get(email=email)
                    request.session['transport_id'] = user.id
                    request.session['transport_name'] = user.username
                    if user.password == password_m:
                        return redirect('index_page')
                    else:
                        message = '用户名或密码错误，请重新输入'
                except:
                    message = '你还没有注册，请先注册'
        if 'btn2' in request.POST:
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                n = hashlib.md5()
                n.update(password.encode())
                password_n = n.hexdigest()
                try:
                    up_name = up_user.objects.get(email=email)
                    request.session['name_record'] = up_name.username

                    if up_name.password == password_n:
                        return redirect('up_user_page')
                    else:
                        message = '用户名或密码错误，请重新输入'
                except:
                    message = '你还不是超级管理用户'

    login_form = LoginForm()
    context = {
        'login_form': login_form,
        'message': message
    }
    return render(request, 'login_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def update_page(request, pk):
    message = ''
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    users_account = user_account.objects.get(id=pk)
    if request.method == 'POST':
        username = request.POST.get('username')
        birthday = request.POST.get('birthday')
        sex = request.POST.get('sex')
        introduction = request.POST.get('introduction')

        user_account.objects.filter(id=pk).update(username=username, birthday=birthday, sex=sex,
                                                  introduction=introduction)
        return redirect('index_page')
    context = {
        'users_account': users_account,
        'message': message,
        'name': value_name,
        'id': value_id
    }

    return render(request, 'update_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def change_password(request, pk):
    message = ''
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    users_account = user_account.objects.get(id=pk)
    if request.method == 'POST':
        password_old = request.POST.get('password_old')
        password_new = request.POST.get('password')
        password_again = request.POST.get('password1')

        user = user_account.objects.get(id=pk)
        if user.password == password_old:
            if password_new == password_again:
                user_account.objects.filter(id=pk).update(password=password_new)
                return redirect('index_page')
            else:
                message = '两次密码输入不一致'
        else:
            message = '原始密码输入错误，请重新输入'
    context = {
        'users_account': users_account,
        'message': message,
        'id': value_id,
        'name': value_name
    }

    return render(request, 'change_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def logout_user(request):
    logout(request)
    return redirect('welcome_page')

#@login_required(login_url='login_page')  # 强制登录才能显示
def message_show(request, pk):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    users_account = user_account.objects.get(id=pk)

    context = {
        'users_account': users_account,
        'id': value_id,
        'name': value_name
    }
    return render(request, 'person_message.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def up_user_page(request):
    accounts = user_account.objects.all()
    users = user_account.objects.all()
    # session 传值
    name2 = request.session['name_record']
    # 数据库读取数值
    r_count = user_account.objects.all().count()
    male_count = user_account.objects.filter(sex='男').count()
    female_count = user_account.objects.filter(sex='女').count()

    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')

    cursor = db.cursor()
    cursor1 = db.cursor()
    cursor2 = db.cursor()
    cursor3 = db.cursor()
    cursor4 = db.cursor()

    sql_l18 = '''
            SELECT COUNT(*) FROM users_user_account WHERE 2022-birthday <18 ;
            '''
    sql_18_25 = '''
        SELECT COUNT(*) FROM users_user_account WHERE 2022-birthday BETWEEN 18 AND 25;
    '''
    sql_30_50 = '''
        SELECT COUNT(*) FROM users_user_account WHERE 2022-birthday BETWEEN 30 AND 50 ;
    '''
    sql_25_30 = '''
        SELECT COUNT(*) FROM users_user_account WHERE 2022-birthday BETWEEN 25 AND 30 ;
    '''
    sql_b50 = '''
        SELECT COUNT(birthday) FROM users_user_account WHERE 2022-birthday >50 ;
    '''
    cursor.execute(sql_l18)
    cursor1.execute(sql_18_25)
    cursor2.execute(sql_25_30)
    cursor3.execute(sql_30_50)
    cursor4.execute(sql_b50)

    results = cursor.fetchall()
    results1 = cursor.fetchall()
    results2 = cursor.fetchall()
    results3 = cursor.fetchall()
    results4 = cursor.fetchall()
    db.close()

    context = {
        'name2': name2,
        'male_count': male_count,
        'female_count': female_count,
        'r_count': r_count,
        'users': users,
        'accounts': accounts,
    }
    return render(request, 'up_user_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def delete_page(request, pk):
    users_delete = user_account.objects.get(id=pk)
    if request.method == 'POST':
        users_delete.delete()
        return redirect('up_user_page')
    context = {
        'users_delete': users_delete,
    }

    return render(request, 'delete_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def add_up_user(request):
    add2 = addForm()
    name2 = request.session['name_record']
    message = ''
    if request.method == 'POST':
        add2 = addForm(request.POST)
        if add2.is_valid():
            name = add2.cleaned_data['username']
            password = add2.cleaned_data['password']
            password1 = add2.cleaned_data['password1']
            email = add2.cleaned_data['email']
            email1 = up_user.objects.filter(email=email)
            add_users = up_user.objects.filter(username=name)
            m = hashlib.md5()
            m.update(password.encode())
            password_m = m.hexdigest()
            if email1:
                message = '该邮箱已存在'
            elif add_users:
                message = '该用户已存在'
            elif password1 != password:
                message = '两次输入密码不一致'
            else:
                user = up_user.objects.create(username=name, password=password_m, email=email)
                user.save()
                return redirect('up_user_page')
    context = {  # 把后端数据传到前端页面显示
        'name2': name2,
        'add2': add2,
        'message': message,
    }
    return render(request, 'add_up_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def add_normal_user(request):
    # message = ''
    # name2 = request.session['name_record']
    #
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     password1 = request.POST.get('password1')
    #     m = hashlib.md5()
    #     m.update(password.encode())
    #     password_m = m.hexdigest()
    #     #进行判断,用户名可以重复
    #     email = user_account.objects.filter(email=email)
    #     if email:
    #         message = '该邮箱已存在'
    #     elif password != password1:
    #         message = '两次输入的密码不一致，请重新输入'
    #     else:
    #         user = user_account.objects.create(username=username, password=password_m, email=email)
    #         user.save()
    #         message = '普通用户添加成功'
    # context = {
    #     'name2': name2,
    #     'message': message,
    # }
    name2 = request.session['name_record']
    register_form = RegisterForm()
    message = ''
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            name = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            password1 = register_form.cleaned_data['password1']
            phone = register_form.cleaned_data['phone']
            email = register_form.cleaned_data['email']

            users = user_account.objects.filter(username=name)
            phone1 = user_account.objects.filter(phone=phone)
            email1 = user_account.objects.filter(email=email)
            m = hashlib.md5()
            m.update(password.encode())
            password_m = m.hexdigest()

            if users:
                message = '该用户名已存在'
            elif phone1:
                message = '该手机号已存在'
            elif email1:
                message = '该邮箱已存在'
            elif password1 != password:
                message = '两次输入密码不一致'
            else:
                user = user_account.objects.create(username=name, password=password_m, phone=phone, email=email)
                user.save()
                return redirect('up_user_page')
    context = {  # 把后端数据传到前端页面显示
        'name2': name2,
        'register_form': register_form,
        'message': message,
    }
    return render(request, 'add_normal_page.html', context)

#@login_required(login_url='login_page')  # 强制登录才能显示
def want_page(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    movies = movie.objects.all()
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    sql = '''
        SELECT * FROM function_app_movie order by score DESC,rated DESC limit 0,10;
        '''
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()

    context = {
        'name': value_name,
        'id': value_id,
        'movies': movies,
        'results': results,
    }
    return render(request, 'tui_jian_page.html', context)

def create():
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    # 创建数据库表
    cursor.execute("DROP TABLE IF EXISTS movies_message")
    sql = '''
                create table movies_message(
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
    cursor.execute(sql)
    print('创建成功')

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
            insert into movies_message(
            url_link,photo_link,chinese_name,origin_name,score,rated,introduction,actors)
            values (%s)''' % ",".join(data)
        cursor.execute(sql)
        db.commit()
    print('爬取数据成功')
    db.close()

#@login_required(login_url='login_page')  # 强制登录才能显示
def data_update(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    message = ''
    status = ''
    if request.method == 'POST':
        if 'update' in request.POST:
            try:
                status = 1
                create()
                getData()
                return redirect('index_page')
            except:
                message = '数据更新失败。'
        else:
            status = 0
    context = {
        'message': message,
        'id': value_id,
        'name': value_name,
        'status': status,
    }
    return render(request, 'movie_data_update.html', context)



