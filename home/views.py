from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import  *

# Create your views here.
import datetime
from django.views.generic.base import View

# a function just to get all countries as a list
countries = []
with open('home/countries.txt', 'r') as country:
    read = country.readline()
    while read:
        countries.append(read.strip('\n'))
        read = country.readline()


class BaseView(View):
    pass

class HomeView(LoginRequiredMixin,BaseView):

    def get(self,request):
        return render(request, 'index.html')



class SignUpView(BaseView):
    def post(self,request,*args,**kwargs):
        self.add_new_user(request)

        return redirect('/login'):w

    def add_new_user(self,request):
        fname , lname = request.POST['fname'] , request.POST['lname']
        username = request.POST['username']
        email , phone = request.POST['email'] , request.POST['phone']
        gender = request.POST['gender']
        city , address  = request.POST['country'], request.POST['address']

        dob = request.POST['dob']
        password , confirm_password = request.POST['password'] , request.POST['password']

        if password == confirm_password:
            if not User.objects.filter(username = username,email = email).exists():
                # creating a new auth user
                auth_user = User.objects.create_user(username = username,first_name = fname,last_name = lname,email = email)
                auth_user.save()
                # get the recently created user
                user = User.objects.get(username = username)

                profile_user = Profile.objects.create(user = user,city = city,address = address,dob = dob,gender = gender)
                profile_user.save()

            else:
                messages.error(request,'username or email already exists')
                return redirect('/')
        else:
            messages.error(request,'Enter Same password on both fields')
            return redirect('/signup')


        messages.success(request ,'Signed Up Successfully')



    def get(self,request):
        signup_view = {}
        today  = datetime.datetime.now()
        max_date = today.strftime("%Y-%m-%d")
        signup_view['max_date'] = max_date
        signup_view['min_date'] = '1900-01-01'
        signup_view['Countries'] = countries

        return render(request,'sign-up.html',signup_view)


