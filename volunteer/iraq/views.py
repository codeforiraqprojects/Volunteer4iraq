# Create your views here.
from django.shortcuts import render, redirect
from .models import Intity,Region,Classification,CustomUser
from django.views.generic import  ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q # new
from django.http import  HttpResponseRedirect
from django.http.response import Http404
from django.contrib.auth import authenticate, login, logout
from iraq.EmailBackEnd import EmailBackEnd
from django.contrib import messages
from django.urls import reverse
import requests
from django.conf import settings
from .forms import CreateNewUser
from .decorators import notLoggedUsers

# import json
# from django.contrib.auth.models import Group
# from django.core.files.storage import FileSystemStorage
# from django.contrib.auth.forms import UserCreationForm
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage





def home(request):
    context = {
    'title': 'الرئيسية',
    }
    return render(request,'iraq/index.html', context)


def details(request):
    context = {
    'title':'قراءة المزيد',
    }
    return render(request, 'iraq/details.html', context)



def Intities(request):
    region = Region.objects.all()
    classification= Classification.objects.all()
    intitys = Intity.objects.all().order_by('-created_at')
    paginator = Paginator(intitys, 6)
    page = request.GET.get('page')
    try:
        intitys = paginator.page(page)
    except PageNotAnInteger:
        intitys = paginator.page(1)
    except EmptyPage:
        intitys = paginator.page(paginator.num_page)
    context = {
        'num_intity': Intity.objects.filter().count(),
        'intitys' : intitys,
        'page': page,
        'region': region,
        'classification': classification,
        'title':'المؤسسات'
    }
    return render(request, 'iraq/intities.html', context)



class SearchIntitiesResultsView2(ListView):
    model = Intity
    model = Region
    model = Classification
    template_name = 'iraq/search_intities_results.html'
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_queryset(self,*args,**kwargs): # new
        query = self.request.GET.get('q')
        object_list = Intity.objects.filter(
            Q(name__icontains=query)  | Q(classification__icontains=query)|Q(region__icontains=query)
        )
        try:
            return object_list
        except Http404:
            self['page'] =1
            return object_list


def about(request):
    context = {
    'title':'من نحن',
    }
    return render(request, 'iraq/about.html', context)




def register_type(request):
    context = {
    'title':'نوع الحساب',
    }
    return render(request, 'iraq/register_type.html', context)




def RegisterIntities(request):
    # if request.user.is_authenticated:
        # //this code save the user. So, enter directly without anything(information)
        # return redirect('/admin_home')
    form=CreateNewUser()
    if request.method=="POST":
        form = CreateNewUser(request.POST)
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password1")
        fcm_token=request.POST.get("password2")
        r = CustomUser.objects.filter(username=username)
        if r.count():
            messages.error(request , 'يوجد مستخدم مسجل بهذا الاسم.')
            return HttpResponseRedirect(reverse("register_intities"))
        r = CustomUser.objects.filter(email=email)
        if r.count():
            messages.error(request ,'هذا الايميل مسجل مسبقا')
            return HttpResponseRedirect(reverse("register_intities"))
        if password and  fcm_token and password != fcm_token:
            messages.error(request , 'كلمة المرور غير متطابقة')
            return HttpResponseRedirect(reverse("register_intities"))
        else:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response' : recaptcha_response
                }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
                    user.adminhod.fcm_token=fcm_token
                    user.save()
                    messages.success(request , f'تهانينا  {user} تم التسجيل بنجاح . ')
                    return HttpResponseRedirect(reverse("doLogin"))
                except:
                    messages.error(request ,  ' هناك خطأ في اسم المستخدم او كلمة المرور!')
                    return HttpResponseRedirect(reverse("register_intities"))
            else:
                messages.error(request ,  ' invalid Recaptcha please try again!')
    context = {
        'form':form,
        'title':'تسجيل المؤسسة',
        }
    return render(request, "iraq/register_intities.html", context)







def doLogin(request):
        form = CreateNewUser()
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response' : recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
                username = request.POST.get('email')
                password = request.POST.get('password1')
                user=EmailBackEnd.authenticate(request,username=username,password=password)
                if user != None:
                    login(request, user)
                    if user.user_type =="1":
                        return HttpResponseRedirect('/admin_home')
                    elif user.user_type =="2":
                        return HttpResponseRedirect(reverse("user_home"))
                else:
                    messages.error(request ,  ' هناك خطأ في البريد الالكتروني او كلمة المرور !')
            else:
                messages.error(request ,' invalid Recaptcha please try again!')
                return HttpResponseRedirect("doLogin")
        context= {
            'title':'دخول',
            'form':form,
        }
        return render(request, 'iraq/login_page.html',context)








def RegisterUser(request):
    # if request.user.is_authenticated: //this code save the user. So, enter directly without anything(information)
    #     return redirect('/user_home')
    form=CreateNewUser()
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password1")
        fcm_token=request.POST.get("password2")
        r = CustomUser.objects.filter(username=username)
        if r.count():
            messages.error(request , 'يوجد مستخدم مسجل بهذا الاسم.')
            return HttpResponseRedirect(reverse("register_user"))
        r = CustomUser.objects.filter(email=email)
        if r.count():
            messages.error(request ,'هذا الايميل مسجل مسبقا')
            return HttpResponseRedirect(reverse("register_user"))
        if password and  fcm_token and password != fcm_token:
            messages.error(request , 'كلمة المرور غير متطابقة')
            return HttpResponseRedirect(reverse("register_user"))
        else:
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response' : recaptcha_response
                }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
            result = r.json()
            if result['success']:
                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
                    user.people.fcm_token=fcm_token
                    user.save()
                    messages.success(request , f'تهانينا  {user} تم التسجيل بنجاح . ')
                    return HttpResponseRedirect(reverse("doLogin"))
                except:
                    messages.error(request ,  ' هناك خطأ في اسم المستخدم او كلمة المرور!')
                    return HttpResponseRedirect(reverse("register_user"))
            else:
                messages.error(request ,  ' invalid Recaptcha please try again!')
    context = {
    'form':form,
    'title':'تسجيل المستخدم',
    }
    return render(request, "iraq/register_user.html", context)
















