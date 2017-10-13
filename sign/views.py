from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
#https://github.com/defnngj/guest

# Create your views here.
def index(request):
    return render(request, "index.html")

#��¼����
def login(request):
    return render(request, "login.html")

#��¼����
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
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})

#��������������
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})

#�α���������
@login_required
def search_realname(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get("realname", "")
    guest_list = Event.objects.filter(realname__contains=search_realname)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})