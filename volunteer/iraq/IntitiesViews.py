from typing import Any
from django.http.response import Http404
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
# from .forms import UserUpdateForm,ProfileUpdateForm
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
from django.template import loader
# from stories.models import Story, StoryStream
# from django.contrib.auth.models import User
# from django import template
# from .decorators import notLoggedUsers
# import json
# import requests
# # from .forms import AddMemberForm,IntitiesForm
# from django.urls import reverse
# # from .filters import IntityFilter
# from .decorators import notLoggedUsers,allowedUsers,IntityAdmins
# # from .forms import IntityForm
# # from .forms import UserUpdateForm, ProfileUpdateForm

# # Create by using class based view replace function based view that provide Django
# # from django.views.generic import CreateView,UpdateView
# # from django.contrib.auth.mixins import LoginRequiredMixin








# # ========Views for Admin=================#

@login_required(login_url='doLogin')
def dashboard(request):
    members=Member.objects.all()
    context = {
        'members':members,
        'title':'dashboard',
    }
    return render(request, 'hod_template/dashboard.html', context)


@login_required(login_url='doLogin')
def admin_home(request):
    context = {
        'title':'الرئيسية',
    }
    return render(request,"hod_template/home_content.html",context)


@login_required(login_url='doLogin')
def Details(request):
    context = {
    'title':'قراءة المزيد',
    }
    return render(request, 'hod_template/details.html', context)


@login_required(login_url='doLogin')
def Profile(request):
    context = {
        'region': Region.objects.all(),
        'gender':Gender.objects.all(),
        'adminhod': AdminHOD.objects.all(),
        'title':'الملف الشخصي',
    }
    return render(request,'hod_template/profile.html', context)


@login_required(login_url='do_login')
def ProfileUpdate(request,user_id):
    user=AdminHOD.objects.get(admin=user_id)
    if user==None:
        return HttpResponse("Intity Not Found")
    else:
        return HttpResponseRedirect("/profile")




@login_required(login_url='doLogin')
def ProfileEdit(request):
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
            adminhod = AdminHOD.objects.get(admin=user_id)
            if request.FILES.get('profile'):
                file = request.FILES['profile']
                fs = FileSystemStorage()
                profile_pic = fs.save(file.name, file)
            else:
                    profile_pic=None
            if profile_pic!=None:
                adminhod.profile_pic= profile_pic
            adminhod.phone=request.POST.get('phone','')
            adminhod.region=request.POST.get('region','')
            adminhod.birth=request.POST.get('birth','')
            adminhod.gender=request.POST.get('gender','')
            adminhod.employee=request.POST.get('employee','')
            adminhod.facebook=request.POST.get('facebook','')
            adminhod.save()
            messages.success(request,"تم التعديل بنجاح")
            return HttpResponseRedirect(reverse("profile_update",kwargs={"user_id":user_id}))
        except:
            messages.error(request,"لا يوجد الملف الشخصي")
            return HttpResponseRedirect(reverse("profile",kwargs={"user_id":user_id}))








@login_required(login_url='doLogin')
def Intities(request):
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
    return render(request, 'hod_template/intities.html', context)

class SearchIntitiesResultsView(ListView):
    model = Intity
    model = Region
    model = Classification
    template_name = 'hod_template/search_intities_results.html'

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
def ViewImageP(request):
    context = {
        'intitys' : Intity.objects.all(),
        'title':'الترخيص'
    }
    return render(request, 'hod_template/permission.html', context)


@login_required(login_url='doLogin')
def More_Read_Intities(request,intity_id):
    intity=Intity.objects.get(id=intity_id)
    context = {
        'intity' : intity,
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),
        'title':'معلومات المؤسسة'
    }
    return render(request, 'hod_template/more_read_intities.html', context)




@login_required(login_url='doLogin')
def Profile_Intities(request):
    context = {
        'title':'معلومات المؤسسة',
        'intitys': Intity.objects.all(),
        'region': Region.objects.all(),
        'classification': Classification.objects.all(),
    }
    return render(request,"hod_template/profile_intities_template.html", context)




@login_required(login_url='doLogin')
def Add_Intities_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile1']
        fs=FileSystemStorage()
        intities_picture=fs.save(file.name,file)
        file=request.FILES['profile2']
        fs=FileSystemStorage()
        permission=fs.save(file.name,file)
        try:
            region=Region.objects.get(id=request.POST.get('region',''))
            classification=Classification.objects.get(id=request.POST.get('classification',''))
            intity=Intity(admin=request.user,name=request.POST.get('name',''),created=request.POST.get('created',''),works=request.POST.get('works',''),abstract=request.POST.get('abstract',''),intities_pic=intities_picture,region=region,classification=classification,permission=permission)
            intity.save()
            messages.success(request,"تم الاضافة بنجاح")
        except Exception as e:
            print(e)
            messages.error(request,"لم يتم الاضافة لا يحق لك معلومات واحدة")
        return HttpResponseRedirect("/profile_intities")



@login_required(login_url='doLogin')
def delete_intities(request, intity_id):
    intity=Intity.objects.get(id=intity_id)
    intity.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/profile_intities")





@login_required(login_url='doLogin')
def Update_Intities(request,intity_id):
    intity=Intity.objects.get(id=intity_id)
    if intity==None:
        return HttpResponse("المؤسسة غير موجودة")
    else:
        return HttpResponseRedirect("/profile_intities")











@login_required(login_url='doLogin')
def Edit_Intities_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        intity=Intity.objects.get(id=request.POST.get('id',''))
        if intity==None:
            return HttpResponse("<h2>المؤسسة غير موجودة</h2>")
        else:
            if request.FILES.get('profile1'):
                file = request.FILES['profile1']
                fs = FileSystemStorage()
                intities_pic = fs.save(file.name, file)
            else:
                intities_pic=None
            if request.FILES.get('profile2'):
                file1 = request.FILES['profile2']
                fs = FileSystemStorage()
                permission = fs.save(file1.name, file1)
            else:
                permission=None
            if (intities_pic!=None):
                intity.intities_pic = intities_pic
            if ( permission!=None):
                intity.permission=permission
            user =request.POST.get('user','')
            intity.name=request.POST.get('name','')
            intity.region=request.POST.get('region','')
            intity.classification=request.POST.get('classification','')
            intity.created=request.POST.get('created','')
            intity.works=request.POST.get('works','')
            intity.abstract=request.POST.get('abstract','')
            intity.save()
            messages.success(request,"تم التحديث بنجاح")
            return HttpResponseRedirect("update_intities/"+str(intity.id)+"")






# @login_required(login_url='doLogin')
# @allowedUsers(allowedGroups=['intityAdmin'])
# def ComReply(request):
#     if request.method!="POST":
#         return HttpResponse("<h2>Method Now Allowed</h2>")
#     else:
#         # comment_name=Comment.objects.get(id=request.POST.get('comm_name',''))
#         # comment_name=Comment.Post.get('comm_name','')
#         # comments = Comment.objects.all()
#         comment_name = Comment(request.POST.get('comm_name',''))
#         rep = Reply(comment_name=comment_name,author=request.user,reply_body=request.POST.get('reply_body',''))
#         rep.save()
#     return redirect("/comments")

# class SearchMemberView(ListView):
    # model = Member
    # model = Intity
    # template_name = 'hod_template/manage_member.html'

    # def get_queryset(self): # new
    #     query = self.request.GET.get('q')
    #     object_list = Member.objects.filter(Q(mem__icontains=query,))
    #     return object_list





@login_required(login_url='doLogin')
def Manage_Members(request,member_id):
    adminhod=CustomUser.objects.get(id=member_id)
    members=adminhod.member_set.all()
    # members = Member.objects.order_by('-created_at').filter()
    paginator = Paginator(members, 10)
    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_page)
    context = {
        'adminhod':adminhod,
        'members': members,
        'regions': Region.objects.all(),
        'genders': Gender.objects.all(),
        'page': page,
        'title':'الاعضاء'
    }
    return render(request,"hod_template/manage_member.html", context)




@login_required(login_url='doLogin')
def Add_Member_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        member_img=fs.save(file.name,file)
        try:
            member_id=request.POST.get('id')
            region=Region.objects.get(id=request.POST.get('region',''))
            gender=Gender.objects.get(id=request.POST.get('gender',''))
            member=Member(name=request.POST.get('name',''),employee=request.POST.get('employee',''),
            phone=request.POST.get('phone',''),email=request.POST.get('email',''),
            member_image=member_img,region=region,gender=gender,admin=request.user)
            member.save()
            messages.success(request,"تم الاضافة بنجاح")
            return HttpResponseRedirect(reverse("manage_members",kwargs={"member_id":member_id}))
        except Exception as e:
            print(e)
            messages.error(request,"فشل في الاضافة")
        return HttpResponseRedirect(reverse("manage_members",kwargs={"member_id":member_id}))



@login_required(login_url='doLogin')
def delete_member(request,member_id):
    member=Member.objects.get(id=member_id)
    if member==None:
        return HttpResponse("Member Not Found")
    else:
        context = {
        'regions': Region.objects.all(),
        'genders': Gender.objects.all(),
        'intitys':Intity.objects.all(),
        'member':member,
        }
        return render(request,"hod_template/delete_member.html", context)

   
@login_required(login_url='doLogin')
def deletes(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        member=Member.objects.get(id=request.POST.get('id',''))
        member.delete()
        members=CustomUser.objects.get(id=request.POST.get('user_id',''))
        messages.error(request, "تم الحذف بنجاح")
        return HttpResponseRedirect("manage_members/"+str(members.id)+"")
    
    
    
@login_required(login_url='doLogin')
def update_member(request,member_id):
    member=Member.objects.get(id=member_id)
    if member==None:
        return HttpResponse("Member Not Found")
    else:
        context = {
        'regions': Region.objects.all(),
        'genders': Gender.objects.all(),
        'intitys':Intity.objects.all(),
        'member':member,
        }
        return render(request,"hod_template/edit_member.html", context)




@login_required(login_url='doLogin')
def edit_member(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        members=CustomUser.objects.get(id=request.POST.get('user_id',''))
        member=Member.objects.get(id=request.POST.get('id',''))
        if member==None:
            return HttpResponse("<h2>Poster Not Found</h2>")
        else:
            try:
                if request.FILES.get('profile')!=None:
                    file = request.FILES['profile']
                    fs = FileSystemStorage()
                    member_img = fs.save(file.name, file)
                else:
                    member_img=None
                if member_img!=None:
                    member.member_image=member_img
                member.admin =request.user
                member.name=request.POST.get('name','')
                member.gender=request.POST.get('gender','')
                region=Region.objects.get(id=request.POST.get('region',''))
                member.region=region
                member.employee=request.POST.get('employee','')
                member.phone=request.POST.get('phone','')
                member.email=request.POST.get('email','')
                member.save()
                messages.success(request,"تم التعديل بنجاح")
                return HttpResponseRedirect("manage_members/"+str(members.id)+"")
            except Exception as e:
                print(e)
                messages.error(request,"فشل في التعديل")
                return HttpResponseRedirect("manage_members/"+str(members.id)+"")
                    


@login_required(login_url='doLogin')
def Declaration(request):
    regions = Region.objects.all()
    posters=Poster.objects.order_by('-created_at')
    classifications= Classification.objects.all()
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
        'classifications': classifications,
        'title':'الاعلانات',
    }
    return render(request, 'hod_template/poster.html', context)



@login_required(login_url='doLogin')
def my_declaration(request,poster_id):
    adminhod=CustomUser.objects.get(id=poster_id)
    posters=adminhod.poster_set.all()
    regions = Region.objects.all()
    # posters=Poster.objects.order_by('-created_at')
    classifications= Classification.objects.all()
    paginator = Paginator(posters, 6)
    page = request.GET.get('page')
    try:
        posters = paginator.page(page)
    except PageNotAnInteger:
        posters = paginator.page(1)
    except EmptyPage:
        posters = paginator.page(paginator.num_page)
    context = {
        'adminhod':adminhod,
        'posters': posters,
        'regions': regions,
        'page': page,
        'num_poster': Poster.objects.filter().count(),
        'classifications': classifications,
        'title':'الاعلانات',
    }
    return render(request, 'hod_template/my_poster.html', context)





@login_required(login_url='doLogin')
def Save_Poster(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        poster_img=fs.save(file.name,file)
        try:
            poster_id=request.POST.get('id')
            region=Region.objects.get(id=request.POST.get('region',''))
            classification=Classification.objects.get(id=request.POST.get('classification',''))
            poster = Poster(name=request.POST.get('name',''),place=request.POST.get('place',''),posts=request.POST.get('posts',''),date_poster=request.POST.get('date_poster',''),poster_image=poster_img,region=region, classification=classification,admin=request.user)
            poster.save()
            messages.success(request,"تم الاضافة بنجاح")
            return HttpResponseRedirect("/poster")
        except Exception as e:
            print(e)
            messages.error(request,"فشل في الاضافة")
            return HttpResponseRedirect("/poster")




@login_required(login_url='doLogin')
def update_poster(request,poster_id):
    poster=Poster.objects.get(id=poster_id)
    if poster==None:
        return HttpResponse("Member Not Found")
    else:
        context = {
            'classifications': Classification.objects.all(),
            'regions': Region.objects.all(),
            'poster':poster
        }
        return render(request,"hod_template/edit_poster.html", context)



@login_required(login_url='doLogin')
def edit_poster(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        poster=Poster.objects.get(id=request.POST.get('id',''))
        if poster==None:
            return HttpResponse("<h2>Poster Not Found</h2>")
        else:
            if request.FILES.get('profile')!=None:
                file = request.FILES['profile']
                fs = FileSystemStorage()
                poster_img = fs.save(file.name, file)
            else:
                poster_img=None

            if poster_img!=None:
                poster.poster_image=poster_img
            poster.name=request.POST.get('name','')
            poster.place=request.POST.get('place','')
            poster.posts=request.POST.get('posts','')
            poster.date_poster=request.POST.get('date_poster','')
            poster.time_poster=request.POST.get('time_poster','')
            region=Region.objects.get(id=request.POST.get('region',''))
            poster.region=region
            poster.classification=request.POST.get('classification','')
            poster.save()
            messages.success(request,"تم التحديث بنجاح")
            return HttpResponseRedirect("/poster")




@login_required(login_url='doLogin')
def DeletePoster(request,poster_id):
    poster=Poster.objects.get(id=poster_id)
    poster.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/poster")



class SearchPosterEduResultsView(ListView):
    model = Poster
    # regions = Region.objects.all(),
    # poster=Poster.objects.all()
    # num_poster = poster.filter(classification='تعليم').count()
    template_name = 'hod_template/search_posterEdu_results.html'
    queryset = Poster.objects.filter(classification__icontains='تعليم')# new
    # num_poster = Poster.objects.filter(classification__icontains='تعليم').count()
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    # def count(request):
    #     poster=Poster.objects.all()
    #     num_poster = poster.filter(classification='تعليم').count()
    #     return render(request,'search_posterEdu_results.html',{'num_poster':num_poster})
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterEduResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterEduResultsView,self).get_context_data(*args,**kwargs)



class SearchPosterEnvResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterEnv_results.html'
    queryset = Poster.objects.filter(classification__icontains='بيئة') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterEnvResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterEnvResultsView,self).get_context_data(*args,**kwargs)


class SearchPosterHeaResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterHea_results.html'
    queryset = Poster.objects.filter(classification__icontains='صحة') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterHeaResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterHeaResultsView,self).get_context_data(*args,**kwargs)


class SearchPosterArtResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterArt_results.html'
    queryset = Poster.objects.filter(classification__icontains='فنون') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterArtResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterArtResultsView,self).get_context_data(*args,**kwargs)


class SearchPosterOthResultsView(ListView):
    model = Poster
    template_name = 'hod_template/search_posterOth_results.html'
    queryset = Poster.objects.filter(classification__icontains='أخرى') # new
    ordering = ['id']
    paginate_by = 6
    paginate_orphans = 1
    def get_context_data(self, *args, **kwargs):
        try:
            return super(SearchPosterOthResultsView,self).get_context_data(*args,**kwargs)
        except Http404:
            self.kwargs['page'] =1
            return super(SearchPosterOthResultsView,self).get_context_data(*args,**kwargs)




@login_required(login_url='doLogin')
def Notification(request):
    # numvolunteers = NumVolunteer.objects.all()
    numvolunteers = NumVolunteer.objects.order_by('-created_at')
    paginator = Paginator(numvolunteers, 1)
    page = request.GET.get('page')
    try:
        numvolunteers = paginator.page(page)
    except PageNotAnInteger:
        numvolunteers = paginator.page(1)
    except EmptyPage:
        numvolunteers = paginator.page(paginator.num_page)
    context = {
        'num_volunteer':NumVolunteer.objects.filter().count(),
        'region': Region.objects.all(),
        'gender':Gender.objects.all(),
        'numvolunteers': numvolunteers,
        'page': page,
        'title':'الاشعارات'
    }
    return render(request, 'hod_template/notification.html', context)




@login_required(login_url='doLogin')
def AddVolunteer(request):
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
            messages.success(request,"تم الاضافة بنجاح")
        except Exception as e:
            print(e)
            messages.error(request,"فشل في ارسال الاشعار")
        return HttpResponseRedirect("/notification")



@login_required(login_url='doLogin')
def DeleteVolunteer(request,notification_id):
    notification=NumVolunteer.objects.get(id=notification_id)
    notification.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/notification")



@login_required(login_url='doLogin')
def comments(request):
    comments=Comment.objects.order_by('-created_at')
    # comments = Comment.objects.all()
    comments_user = Comment_User.objects.order_by('-created_at')
    # comments_user = Comment_User.objects.all()
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
        'customuser':customuser,
        'comments' : comments,
        'comments_user' : comments_user,
        'num_com': Comment.objects.filter().count() + Comment_User.objects.filter().count(),
        'page': page,
        'title':'التعليقات',
    }
    return render(request, 'hod_template/comments.html', context)








@login_required(login_url='doLogin')
def Add_Comment_Save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        try:
            adminhod = AdminHOD.objects.all()
            people = People.objects.all()
            com = Comment(comm_name=request.POST.get('comm_name',''),author=request.user,body=request.POST.get('body',''), comment_pic=request.user.adminhod)
            com.save()
            messages.success(request,"تم الاضافة بنجاح")
            return redirect("/comments")
        except Exception as e:
            print(e)
            messages.error(request,"لم يتم الاضافة ")
            return redirect("/comments")



@login_required(login_url='doLogin')
def LikeView(request,pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments'))


@login_required(login_url='doLogin')
def LikeViewUser(request,pk):
    comment= get_object_or_404(Comment_User, id=request.POST.get('comment_user_id'))
    comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('comments'))


@login_required(login_url='doLogin')
def delete_comment(request,comment_id):
    comment=Comment.objects.get(id=comment_id)
    comment.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/comments")


@login_required(login_url='doLogin')
def delete_comment_user(request,comment_user_id):
    comment=Comment_User.objects.get(id=comment_user_id)
    comment.delete()
    messages.error(request, "تم الحذف بنجاح")
    return HttpResponseRedirect("/comments")




@login_required(login_url='doLogin')
def About(request):
    context = {
    'title':'من نحن',
    }
    return render(request, 'hod_template/about.html', context)



