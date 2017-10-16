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

#��¼����
def login(request):
    return render(request, "login.html")

#��¼������ͼ
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)                                      #��¼
            request.session['user'] = username                             #��session��Ϣ��¼�������
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'login.html', {'error': 'username or password error!'})

#�����������ͼ
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username =request.session.get('user', '')                                #��ȡ�����session
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#�α�������ͼ
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    username =request.session.get('user', '')
    paginator = Paginator(guest_list, 10)   #�Ѳ�����������У�����Ϊÿҳ��ʾ10��
    page = request.GET.get('page')         #ͨ��get����ǰҪ��ʾ�ڼ�ҳ
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:               #���ҳ�治����������ô��ʾ��һҳ
        contacts = paginator.page(1)
    except EmptyPage:                      #���ҳ�泬����ҳ������ô��ʾ���һҳ
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

#��������������
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#�α��ֻ�������
@login_required
def search_phone(request):
    username = request.session.get('user', '')
    search_phone = request.GET.get("phone", "")
    search_name_bytes = search_phone.encode(encoding="utf-8")
    guest_list = Guest.objects.filter(phone__contains=search_name_bytes)
    username = request.session.get('user', '')

    paginator = Paginator(guest_list, 10)   #�Ѳ�����������У�����Ϊÿҳ��ʾ2��
    page = request.GET.get('page')         #ͨ��get����ǰҪ��ʾ�ڼ�ҳ
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:               #���ҳ�治����������ô��ʾ��һҳ
        contacts = paginator.page(1)
    except EmptyPage:                      #���ҳ�泬����ҳ������ô��ʾ���һҳ
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})

# ǩ��ҳ��
@login_required
def sign_index(request, eid):
    event =get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})

#ǩ������
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
