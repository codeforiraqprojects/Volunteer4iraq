"""volunteer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from volunteer import settings
from  iraq import views
from iraq.views import SearchIntitiesResultsView2
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('iraq.urls')),
    path('',views.home, name='home'),
    path('details/', views.details, name='details'),
    path('intities/', views.Intities, name='intities'),
    path('search_Intities2/', SearchIntitiesResultsView2.as_view(), name='search_Intities_results2'),
    path('about/', views.about, name='about'),
    path('register_type/', views.register_type, name='register_type'),
    path('register_intities',views.RegisterIntities, name='register_intities'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('register_user', views.RegisterUser, name='register_user'),
    path('logout', LogoutView.as_view(template_name= "iraq/logout.html"), name='logout'),

    # # path('oauth/', include('social_django.urls', namespace='social')),
    
    # # # for Reset Password
    path('reset_password/' , auth_views.PasswordResetView.as_view(template_name= "iraq/password_reset.html"), name="reset_password"),
    path('reset_password_sent/' , auth_views.PasswordResetDoneView.as_view(template_name= "iraq/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(template_name= "iraq/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/' , auth_views.PasswordResetCompleteView.as_view(template_name= "iraq/password_reset_done.html"), name="password_reset_complete"),  

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
