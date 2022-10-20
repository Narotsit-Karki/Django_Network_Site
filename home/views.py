from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.http import Http404

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


class BaseView(LoginRequiredMixin,View):
    view = dict()


    def get_user(self,request):
        try:
            auth_user = Profile.objects.get(user = request.user)
            return auth_user
        except ObjectDoesNotExist:
            raise Http404



class HomeView(BaseView):

    def get(self,request):
        self.view
        try:
            auth_user = Profile.objects.get(user = request.user)
            self.view['auth_user'] = auth_user
            return render(request, 'index.html', self.view)

        except ObjectDoesNotExist:
            raise Http404






class SignUpView(View):
    def post(self,request,*args,**kwargs):
        self.add_new_user(request)

        return redirect('/login')

    def add_new_user(self,request):
        fname , lname = request.POST['fname'] , request.POST['lname']
        username = request.POST['username']
        email , phone = request.POST['email'] , request.POST['phone']
        gender = request.POST['gender']
        country , city  = request.POST['country'], request.POST['city']

        print(country,city)

        dob = request.POST['dob']
        password , confirm_password = request.POST['password'] , request.POST['password']

        if password == confirm_password:
            if not User.objects.filter(username = username,email = email).exists():
                # creating a new auth user
                auth_user = User.objects.create_user(username = username,
                                                     first_name = fname,
                                                     last_name = lname,
                                                     email = email,
                                                     password = password)
                auth_user.save()
                # get the recently created user
                user = User.objects.get(username = username)

                profile_user = Profile.objects.create(user = user,
                                                      username = username,
                                                      fname = fname,
                                                      lname = lname,
                                                      email = email,
                                                      city = city,
                                                      country = country,
                                                      dob = dob,
                                                      gender = gender
                                                      )
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
        today = datetime.datetime.now()
        max_date = today.strftime("%Y-%m-%d")
        signup_view['max_date'] = max_date
        signup_view['min_date'] = '1900-01-01'
        signup_view['Countries'] = countries

        return render(request,'sign-up.html',signup_view)



class ProfileView(BaseView):

    def get_user(self , request , username):
        try:
            user_obj = Profile.objects.get(username = username)
            auth_user = Profile.objects.get(user = request.user)
            # see if current user is following the user
            following = False
            if Profile.objects.filter(following__in = [user_obj]).exists():
                following = True

            return user_obj , auth_user , following

        except ObjectDoesNotExist:
            raise Http404

    def get(self,request,username):
        self.view
        self.view['user_obj'] , self.view['auth_user'], self.view['following'] = self.get_user(request,username)
        return render(request, 'profile.html',self.view)


#error 404
def error_404(request,exception):
    return render(request,'404.html')



def follow_unfollow_user(request,username):
    try:
        follow_user = Profile.objects.get(username = username)
        cur_auth_user = Profile.objects.get(user = request.user)
        if Profile.objects.filter(following__in = [follow_user]).exists():
            cur_auth_user.following.remove(follow_user)

        else:
            cur_auth_user.following.add(follow_user)

        cur_auth_user.save()
        return redirect(f'/profile/{username}')
    except ObjectDoesNotExist:
        raise Http404

class SettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request,'settings.html',self.view)
