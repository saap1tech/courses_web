from django.shortcuts import render, redirect
from basic import models
from django.core import serializers
import json
from . import forms

# Create your views here.

def home(request):
    try:
        if not request.session["login"]:
            return render(request, 'home.html')
        else:
            return redirect('/index/')
    except KeyError:
        return render(request, 'home.html')

def reglog(request):
    try:
        if not request.session["login"]:
            msg = ''
            if request.method == 'POST':
                namer = request.POST.get('namer')
                emailr = request.POST.get('emailr')
                pass1 = request.POST.get('pass1')
                pass2 = request.POST.get('pass2')

                email = request.POST.get('email')
                passw = request.POST.get('pass')

                if namer and emailr and pass1 and pass2:
                    select1 = models.Users.objects.filter(name=namer)
                    select2 = models.Users.objects.filter(email=emailr)
                    if pass1 != pass2:
                        msg = 'كلمتا السر مختلفتين'

                    else:
                        users = models.Users()
                        if select1 or select2:
                            msg = 'هذا الحساب موجود'
                        else:
                            users.name = namer
                            users.email = emailr
                            users.password = pass1
                            users.save()

                            login = models.Users.objects.filter(email=emailr, password=pass1)
                            log = serializers.serialize("json", login)
                            request.session["login"] = log
                            return redirect("/index/", request)

                elif email and passw:
                    login = models.Users.objects.filter(email=email, password=passw)
                    if login:
                        log = serializers.serialize("json", login)
                        request.session["login"] = log
                        return redirect("/index/", request)
                    else:
                        msg = 'المعلومات خاطئة'

            context = {
                'msg': msg
            }

            return render(request, 'reglog.html', context)
        else:
            return redirect('/index/')
    except KeyError:
        msg = ''
        if request.method == 'POST':
            namer = request.POST.get('namer')
            emailr = request.POST.get('emailr')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')

            email = request.POST.get('email')
            passw = request.POST.get('pass')

            if namer and emailr and pass1 and pass2:
                select1 = models.Users.objects.filter(name=namer)
                select2 = models.Users.objects.filter(email=emailr)
                if pass1 != pass2:
                    msg = 'كلمتا السر مختلفتين'

                else:
                    users = models.Users()
                    if select1 or select2:
                        msg = 'هذا الحساب موجود'
                    else:
                        users.name = namer
                        users.email = emailr
                        users.password = pass1
                        users.save()

                        login = models.Users.objects.filter(email=emailr, password=pass1)
                        log = serializers.serialize("json", login)
                        request.session["login"] = log
                        return redirect("/index/", request)

            elif email and passw:
                login = models.Users.objects.filter(email=email, password=passw)
                if login:
                    log = serializers.serialize("json", login)
                    request.session["login"] = log
                    return redirect("/index/", request)
                else:
                    msg = 'المعلومات خاطئة'

        context = {
            'msg': msg
        }

        return render(request, 'reglog.html', context)

def index(request):
    try:
        if not request.session["login"]:
            return redirect("/")
        else:
            if request.method == "POST":
                search = request.POST.get("search")
                logout = request.POST.get("logout")
                if logout:
                    request.session["login"] = 0
                    return redirect('/')
                if search:
                    return redirect('/search/'+search+'/')
            row = models.Plays.objects.all()
            login = request.session["login"]
            name = json.loads(login)[0].get("fields", not None).get("name", not None)
            context = {
                'row': row,
                'name': name,
            }
            return render(request, 'index.html', context)
    except KeyError:
        return redirect("/")

def AddPl(request):
    try:
        if not request.session["login"]:
            return redirect("/")
        else:
            msg = ''
            if request.method == "POST":
                title = request.POST.get("title")
                desc = request.POST.get("desc")

                logout = request.POST.get("logout")
                if logout:
                    request.session["login"] = 0
                    return redirect('/')

                if title and desc:
                    plays = models.Plays()
                    se = models.Plays.objects.filter(title=title)
                    if se:
                        msg = "هذه الدورة موجودة"
                    else:
                        login = request.session["login"]
                        name = json.loads(login)[0].get("fields", not None).get("name", not None)

                        plays.title = title
                        plays.description = desc
                        plays.user = name
                        plays.save()

                        msg = "تم إنشاء دورتك بنجاح"

            context = {
                'msg': msg
            }
            return render(request, 'AddPl.html', context)
    except KeyError:
        return redirect("/")

def AddVd(request):
    global msg
    msg = ""
    try:
        if not request.session["login"]:
            return redirect("/")
        else:
            form = forms.AddVideo()

            login = request.session["login"]
            name = json.loads(login)[0].get("fields", not None).get("name", not None)

            ypl = models.Plays.objects.filter(user=name)
            if request.method == "POST":
                logout = request.POST.get('logout')

                video = request.FILES.get('video')
                title = request.POST.get('title')
                play = request.POST.get('play')
                rend = request.POST.get('rend')

                if logout:
                    request.session["login"] = 0
                    return redirect('/')

                if video and title and play and rend:
                    CrVd = models.Videos()
                    CrVd.video = video
                    CrVd.title = title
                    CrVd.play = play
                    CrVd.rend = rend
                    CrVd.save()

                    msg = 'تم تحميل الفيديو بنجاح'

            context = {
                'form': form,
                'select': ypl,
                'msg': msg,
            }
            return render(request, 'AddVd.html', context)
    except KeyError:
        return redirect("/")

def search(request,search):
    try:
        if not request.session["login"]:
            return redirect("/")
        else:
            if request.method == "POST":
                logout = request.POST.get("logout")
                if logout:
                    request.session["login"] = 0
                    return redirect('/')
            row = models.Plays.objects.filter(title=search)
            if row:
                msg = '{} هذه نتائج البحث حول'.format(search)
            else:
                msg = '{} لم أعثر على أي شيء حول'.format(search)

            context = {
                'msg': msg,
                'row': row,
            }
            return render(request, 'search.html', context)
    except KeyError:
        return redirect("/")

def watch(request, play, video):
    try:
        if not request.session["login"]:
            return redirect("/")
        else:
            if request.method == "POST":

                logout = request.POST.get('logout')
                if logout:
                    request.session["login"] = 0
                    return redirect('/')

            row = models.Videos.objects.filter(play=play)
            select = models.Videos.objects.filter(play=play, rend=video)

            context = {
                'row': row,
                'select': select,
            }

            return render(request, 'watch.html', context)
    except KeyError:
        return redirect("/")
