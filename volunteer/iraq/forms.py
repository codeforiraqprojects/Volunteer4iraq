from django import forms
from django.db.models import fields
# from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,AdminHOD,Intity, Member, Poster,Region, Classification
from django.forms import ModelForm


class CreateNewUser(forms.Form):
    username = forms.CharField(label='اسم المستخدم', max_length=255,help_text='اسم المستخدم يجب الا يحتوي على مسافات' ,
                        widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    email = forms.EmailField(label='البريد الإلكتروني',
                        widget= forms.TextInput(attrs={'class': 'form-control mb-3'}))
    password1 = forms.CharField(label='كلمة المرور',help_text='يجب الايقل عن ثمانية',
                        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), min_length=8,required=True)
    password2 = forms.CharField(label='تأكيد كلمة المرور', 
                        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}), min_length=8,required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = CustomUser.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError('يوجد مستخدم مسجل بهذا الاسم.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        if r.count():
            raise forms.ValidationError('هذا الايميل مسجل مسبقا')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('كلمة المرور غير متطابقة')

    class Meta:
            model = CustomUser
            fields = ('username', 'email', 'password1', 'password2')

    


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='اسم المستخدم', max_length=255,help_text='اسم المستخدم يجب الا يحتوي على مسافات' ,
                        widget= forms.TextInput(attrs={'class': 'form-control  mb-3'}))
    email = forms.EmailField(label='البريد الإلكتروني',
                        widget= forms.TextInput(attrs={'class': 'form-control mb-3'}))
  
    class Meta:
        model = CustomUser
        fields = ('username','email')




    



