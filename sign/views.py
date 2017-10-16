from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#https://github.com/defnngj/guest

# Create your views here.
def index(request):
    return render(request, "index.html")

#登录界面
def login(request):
    return render(request, "login.html")

#登录动作试图
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)                                      #登录
            request.session['user'] = username                             #将session信息记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error!'})

#发布会管理视图
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username =request.session.get('user', '')                                #读取浏览器session
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#嘉宾管理视图
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username =request.session.get('user', '')
    paginator = Paginator(guest_list, 10)   #把查出来的所有列，划分为每页显示10条
    page = request.GET.get('page')         #通过get请求当前要显示第几页
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:               #如果页面不是整数，那么显示第一页
        contacts = paginator.page(1)
    except EmptyPage:                      #如果页面超出总页数，那么显示最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

#发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#嘉宾手机号搜索
@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    username = request.session.get('user', '')

    paginator = Paginator(guest_list, 10)   #把查出来的所有列，划分为每页显示2条
    page = request.GET.get('page')         #通过get请求当前要显示第几页
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:               #如果页面不是整数，那么显示第一页
        contacts = paginator.page(1)
    except EmptyPage:                      #如果页面超出总页数，那么显示最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

# 签到页面
@login_required
def sign_index(request, eid):
    event =get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})

#签到动作
@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result =Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'user has sign in'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success', 'guest': result})
