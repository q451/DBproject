import pymysql
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max
from django.shortcuts import render, redirect
from .models import user_account, up_user
from function_app.models import test, movie
from .forms import RegisterForm, LoginForm, addForm
from django.contrib.auth import authenticate, login, logout
import hashlib
from django.core.mail import send_mail
# Create your views here.

# @login_required(login_url='welcome_page') # 强制登录才能显示
def base_page(request):
    context = {

    }
    return render(request, 'base.html', context)


# @login_required(login_url='welcome_page') # 强制登录才能显示
def index_page(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    movies = movie.objects.all()
    counter = 0
    top_20 = []
    for i in movies:
        if counter<20:
            top_20.append(i)
            counter += 1
        else:
            break
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    sql = '''
        SELECT * FROM function_app_movie order by id limit 0,10;
        '''
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results)
    db.close()

    context = {
        'name': value_name,
        'id': value_id,
        'movies': movies,
        'top_20': top_20,
    }
    return render(request, 'index.html', context)

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

def ping_top(request):
    value_id = request.session['transport_id']
    value_name = request.session['transport_name']
    db = pymysql.connect(host='localhost', user='root', password='123456', database='django')
    cursor = db.cursor()
    sql = '''
        SELECT * FROM function_app_movie order by score DESC limit 0,20;
        '''
    cursor.execute(sql)
    #获取所有游标
    results = cursor.fetchall()
    db.close()
    context = {
        'name': value_name,
        'id': value_id,
        'u': results,
    }
    return render(request, 'ping_feng.html', context)

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
                    print(up_name.username)
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


# @login_required(login_url='welcome_page') # 强制登录才能显示
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


# @login_required(login_url='welcome_page') # 强制登录才能显示
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


def logout_user(request):
    logout(request)
    return redirect('welcome_page')


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
    print(results3)
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


def delete_page(request, pk):
    users_delete = user_account.objects.get(id=pk)
    if request.method == 'POST':
        users_delete.delete()
        return redirect('up_user_page')
    context = {
        'users_delete': users_delete,
    }

    return render(request, 'delete_page.html', context)


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