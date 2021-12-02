from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.contrib import messages
# from django.contrib.auth.models import User,Group
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Q # new
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.views.generic import TemplateView, ListView ,CreateView
from django.urls import reverse

# import json
# import requests
# # from .forms import AddMemberForm,IntitiesForm
# from django.urls import reverse
# # from .filters import IntityFilter
# from .decorators import notLoggedUsers,allowedUsers,IntityAdmins
# # from .forms import IntityForm
# # from .forms import UserUpdateForm, ProfileUpdateForm
# # from .forms import UserUpdateForm,ProfileUpdateForm

# # Create by using class based view replace function based view that provide Django
# # from django.views.generic import CreateView,UpdateView
# # from django.contrib.auth.mixins import LoginRequiredMixin


# # ========Views for User=================#

@login_required(login_url='doLogin')
def user_home(request):
    return render(request,"user_template/home_content.html")


@login_required(login_url='doLogin')
def Profile1(request):
    context = {
        'region': Region.objects.all(),
        'gender':Gender.objects.all(),
        'people':People.objects.all(),
        'title':'الملف الشخصي',
    }
    return render(request,'user_template/profile.html', context)


@login_required(login_url='do_login')
def ProfileUpdate1(request,user_id):
    user=People.objects.get(admin=user_id)
    if user==None:
        return HttpResponse("Intity Not Found")
    else:
        return HttpResponseRedirect("/profile1")




@login_required(login_url='doLogin')
def ProfileEdit1(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        user_id=request.POST.get('user_id')
        username =request.POST.get('user')
        email=request.POST.get('email')
        try:
            user=CustomUser.objects.get(id=user_id)
            user.username = username
            user.email = email
            user.save()
            people = People.objects.get(admin=user_id)
            if request.FILES.get('profile'):
                file = request.FILES['profile']
                fs = FileSystemStorage()
                profile_pic = fs.save(file.name, file)
            else:
                    profile_pic=None
            if profile_pic!=None:
                people.profile_pic= profile_pic
            people.phone=request.POST.get('phone','')
            people.region=request.POST.get('region','')
            people.birth=request.POST.get('birth','')
            people.gender=request.POST.get('gender','')
            people.employee=request.POST.get('employee','')
            people.facebook=request.POST.get('facebook','')
            people.save()
            messages.success(request,",تم التعديل بنجاح")
            return HttpResponseRedirect(reverse("profile_update1",kwargs={"user_id":user_id}))
        except:
            messages.error(request,"لا يوجد الملف الشخصي")
            return HttpResponseRedirect(reverse("profile1",kwargs={"user_id":user_id}))







@login_required(login_url='doLogin')
def Intities2(request):
    region = Region.objects.all()
    classification= Classification.objects.all()
    intitys = Intity.objects.all().order_by('-created_at')
    paginator = Paginator(intitys, 12)
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
    return render(request, 'user_template/intities.html', context)



@login_required(login_url='doLogin')
def More_Read_Intities1(request,intity_id):
    intity=Intity.objects.get(id=intity_id)
    context = {
        'intity' : intity,
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),
        'title':'معلومات المؤسسة'
    }
    return render(request, 'user_template/more_read_intities.html', context)


class SearchIntitiesResultsView1(ListView):
    model = Intity
    model = Region
    model = Classification
    template_name = 'user_template/search_intities_results.html'

    ordering = ['id']
    paginate_by = 12
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



@login_required(login_url='doLogin')
def Details2(request):
    context = {
    'title':'قراءة المزيد',
    }
    return render(request, 'user_template/details.html', context)


@login_required(login_url='doLogin')
def Profile_Intities1(request):
    context = {
        'title':'معلومات المؤسسة'
    }
    return render(request,'user_template/profile_intities_template.html', context)


@login_required(login_url='doLogin')
def Declaration1(request):
    regions = Region.objects.all()
    posters=Poster.objects.order_by('-created_at')
    # posters = Poster.objects.all()
    classification= Classification.objects.all()
    paginator = Paginator(posters, 6)
    page = request.GET.get('page')
    try:
        posters = paginator.page(page)
    except PageNotAnInteger:
        posters = paginator.page(1)
    except EmptyPage:
        posters = paginator.page(paginator.num_page)
    context = {
        'posters': posters,
        'regions': regions,
        'page': page,
        'num_poster': Poster.objects.filter().count(),
        'classifications': classification,
        'title':'الاعلانات',
    }
    return render(request, 'user_template/poster.html', context)


class SearchPosterEduResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterEdu_results1.html'
    queryset = Poster.objects.filter(classification__icontains='تعليم') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterEduResultsView1,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterEduResultsView1,self).get_context_data(*args,**kwargs)

class SearchPosterEnvResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterEnv_results1.html'
    queryset = Poster.objects.filter(classification__icontains='بيئة') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterEnvResultsView1,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterEnvResultsView1,self).get_context_data(*args,**kwargs)

class SearchPosterHeaResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterHea_results1.html'
    queryset = Poster.objects.filter(classification__icontains='صحة') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterHeaResultsView1,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterHeaResultsView1,self).get_context_data(*args,**kwargs)

class SearchPosterArtResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterArt_results1.html'
    queryset = Poster.objects.filter(classification__icontains='فنون') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterArtResultsView1,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterArtResultsView1,self).get_context_data(*args,**kwargs)

class SearchPosterOthResultsView1(ListView):
    model = Poster
    template_name = 'user_template/search_posterOth_results1.html'
    queryset = Poster.objects.filter(classification__icontains='أخرى') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterOthResultsView1,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterOthResultsView1,self).get_context_data(*args,**kwargs)


@login_required(login_url='doLogin')
def Add_Notification(request):
    context = {
    'numvolunteers': NumVolunteer.objects.all(),
    'region': Region.objects.all(),
    'gender':Gender.objects.all(),
    'title':'ارسال اشعار للمؤسسة للتطوع'
    }
    return render(request, 'user_template/add_notification.html', context)



@login_required(login_url='doLogin')
def Send_Notification(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        volunteer_img=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            gender=Gender.objects.get(id=request.POST.get('gender',''))
            numvolunteer=NumVolunteer(n_intity=request.POST.get('name_intity',''),name=request.POST.get('name',''),age=request.POST.get('age',''),employee=request.POST.get('employee',''),volunteer_image=volunteer_img,region=region,gender=gender)
            numvolunteer.save()
            messages.success(request,"تم الارسال بنجاح")
        except Exception as e:
            print(e)
            messages.error(request,"فشل في ارسال الاشعار")
        return HttpResponseRedirect("/add_notification")





@login_required(login_url='doLogin')
def comments1(request):
    comments=Comment.objects.order_by('-created_at')
    # comments = Comment.objects.all()
    # comments_user = Comment_User.objects.all()
    comments_user = Comment_User.objects.order_by('-created_at')
    customuser = CustomUser.objects.all()
    # reply = Reply.objects.all()
    paginator = Paginator(comments, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_page)
    context = {
        # 'reply': reply,
        'customuser':customuser,
        'comments' : comments,
        'comments_user' : comments_user,
        'num_com': Comment.objects.filter().count() + Comment_User.objects.filter().count(),
        'page': page,
        'title':'التعليقات',
    }
    return render(request, 'user_template/comments_user.html', context)



@login_required(login_url='doLogin')
def LikeView1(request,pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments1'))


@login_required(login_url='doLogin')
def LikeViewUser1(request,pk):
    comment= get_object_or_404(Comment_User, id=request.POST.get('comment_user_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments1'))


@login_required(login_url='doLogin')
def Add_Comment_Save_User(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        try:
            people = People.objects.all()
            com = Comment_User(comm_name=request.POST.get('comm_name',''),author=request.user,body=request.POST.get('body',''), comment_pic=request.user.people)
            com.save()
            messages.success(request,"تم الاضافة بنجاح")
            return redirect("/comments1")
        except Exception as e:
            print(e)
            messages.error(request,"لم يتم الاضافة ")
            return redirect("/comments1")







@login_required(login_url='doLogin')
def delete_comment_user1(request,comment_user_id):
    comment=Comment_User.objects.get(id=comment_user_id)
    comment.delete()
    messages.error(request, "Deleted Successfully")
    return HttpResponseRedirect("/comments1")



@login_required(login_url='doLogin')
def About2(request):
    context = {
    'title':'من نحن',
    }
    return render(request, 'user_template/about.html', context)
























































