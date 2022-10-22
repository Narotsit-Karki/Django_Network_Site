from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.http import Http404, response, HttpResponse
import os
# Create your views here.
import datetime
from django.views.generic.base import View
from functools import reduce
import operator
from django.db.models import Q
from notifications.signals import notify

notification_messsage = {
    'friend-request-send' : 'sent you a friend request',
    'friend-request-accept': 'accepted your friend request',
    'following-you': 'started following you',
}

# a function just to get all countries as a list
countries = []
with open('home/countries.txt', 'r') as country:
    read = country.readline()
    while read:
        countries.append(read.strip('\n'))
        read = country.readline()


class BaseView(LoginRequiredMixin,View):
    view = dict()
    login_url = '/login'
    redirect_field_name = '/login-info'




class HomeView(BaseView):

    def get(self,request):
        user = UserProfile.objects.get(username = request.user.username)
        self.view['User'] = user
        return render(request, 'index.html',self.view)



@login_required
def mark_as_read(request):
    request.user.notifications.mark_all_as_read()
    return redirect(request.META.get('HTTP_REFERER'))


class SignUpView(View):
    def post(self,request,*args,**kwargs):
        self.add_new_user(request)
        messages.success(request, 'Signed Up Successfully')
        return redirect('/login')


    def add_new_user(self,request):
        fname , lname = request.POST['fname'] , request.POST['lname']
        username = request.POST['username']
        email , phone = request.POST['email'] , request.POST['phone']
        gender = request.POST['gender']
        country , city  = request.POST['country'], request.POST['city']

        dob = request.POST['dob']
        password , confirm_password = request.POST['password'] , request.POST['password']

        if password == confirm_password:
            if not UserProfile.objects.filter(username = username,email = email).exists():
                profile_user = UserProfile.objects.create_user(
                    username = username,
                    first_name = fname,
                    last_name = lname,
                    email = email,
                    city = city,
                    country = country,
                    dob = dob,
                    gender = gender,
                    phone = phone,
                    password = password
                    )
                profile_user.save()

            else:
                messages.error(request,'username or email already exists')
                return redirect('/signup')
        else:
            messages.error(request,'Enter Same password on both fields')
            return redirect('/signup')



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
            user_obj = UserProfile.objects.get(username = username)
            # see if current user is following the user
            following = False
            friend = False
            sent_friend_request = False

            if UserProfile.objects.filter(username = request.user.username , following__in = [user_obj]).exists():
                following = True

            if UserProfile.objects.filter(username = user_obj.username, friends__in = [request.user]).exists():
                friend = True

            if FriendRequest.objects.filter(from_user = request.user,to_user = user_obj).exists():

                sent_friend_request = True

            return user_obj , following , friend , sent_friend_request

        except ObjectDoesNotExist:
            raise Http404

    def get(self,request,username):
        self.view

        self.view['User_Profile'] , self.view['Following'] , self.view['Friend'] , self.view['Friend_Requst_Sent'] = self.get_user(request,username)

        return render(request, 'profile.html',self.view)


#error 404
def error_404(request,exception):
    return render(request,'404.html')


@login_required
def follow_unfollow_user(request):
    if request.method == "GET":
        username = request.GET['username']
        follow_user = UserProfile.objects.get(username = username)
        # if already followed unfollow else follow
        if UserProfile.objects.filter(username = request.user.username,following__in = [follow_user]).exists():
            request.user.following.remove(follow_user)
        else:
            notify.send(sender = request.user , recipient = follow_user , verb = 'pill', description = notification_messsage['following-you'])
            request.user.following.add(follow_user)

        request.user.save()

        return redirect(f'/profile/{username}')










class SearchView(BaseView):

    def search_algorithm(self, query, request):
        keyword = set()

        if "," in query:
            for word in query.split(","):
                keyword.add(word.strip(" "))

        elif " " in query:
            for word in query.split(" "):
                keyword.add(word)
        else:
            keyword = {query}

        # getting necessary search result profiles
        profiles = UserProfile.objects.exclude(username = request.user.username).filter(reduce(operator.and_, ( Q(username__icontains = x) for x in keyword)))

        # get current users friend list to see if searched user is present or not
        user_friend_requests = FriendRequest.objects.filter(to_user__in = list(profiles),from_user = request.user)

        if user_friend_requests.count() == 0:
            self.view['User_Friend_Requests'] = user_friend_requests
        else:
            self.view['User_Friend_Requests'] = UserProfile.objects.filter(reduce(operator.and_,( Q(username = f.to_user.username) for f in user_friend_requests)))

        #get searched users friend requests to see if current user is present there or not
        searched_user_friend_requests = FriendRequest.objects.filter(from_user__in = list(profiles),to_user = request.user)

        if searched_user_friend_requests.count() == 0:
            self.view['Searched_User_Friend_Requests'] = searched_user_friend_requests
        else:
            self.view['Searched_User_Friend_Requests'] = UserProfile.objects.filter(
                reduce(operator.and_, (Q(username=f.from_user.username) for f in searched_user_friend_requests)))

        self.view['Searched_Users'] = profiles


    def get(self,request):
        search = request.GET['search']
        #getting User Friends as  query set for searching purpose
        self.view['User_Friends'] = request.user.friends.get_queryset()
        self.search_algorithm(query=search,request = request)
        return render(request,'search.html',self.view)




@login_required
def send_friend_request_or_remove(request):

    if request.method == "GET":
        username = request.GET['addfriend_username']
        from_user = request.user
        to_user = UserProfile.objects.get(username = username)

        # check to see if not both users are friends already
        if UserProfile.objects.filter(username = from_user.username , friends__in = [to_user]).exists() or UserProfile.objects.filter(username = to_user.username , friends__in = [from_user]).exists():
            return redirect(request.META.get('HTTP_REFERER'))

        # send friend request
        friend_request , created = FriendRequest.objects.get_or_create(from_user = from_user , to_user = to_user)

       # request was already sent now we delete it
        if not created:
            friend_request.delete()
        else:
            notify.send(sender = from_user , recipient = to_user,verb ='Message', description = notification_messsage['friend-request-send'])


    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def accept_friend_request(request):

    if request.method == 'GET':
        try:
            from_username = request.GET['u_name']
            from_user = UserProfile.objects.get(username = from_username)
            friend_request = FriendRequest.objects.get(from_user = from_user, to_user = request.user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.to_user.friends.add(friend_request.from_user)
            notify.send(sender = friend_request.to_user , recipient = friend_request.from_user , verb = 'pill', description = notification_messsage['friend-request-accept'])

            friend_request.delete()
        except Exception:
            pass

    return redirect(request.META.get("HTTP_REFERER"))




#
@login_required
def store_login_info(request):
    if request.user_agent.is_mobile:
        device = 'mobile'
    elif request.user_agent.is_pc:
        device = 'pc'
    elif request.user_agent.is_tablet:
        device = 'tablet'
    elif request.user_agent.is_bot:
        device = 'pc'

    slug = os.urandom(8).hex()
    login_object = LoginSessionInfo.objects.create(
        slug = slug,
        user = request.user,
        os = request.user_agent.os.family,
        device = device,
        device_type = request.user_agent.device.family,
        browser = request.user_agent.browser.family,
        active = True,
        )

    login_object.save()

    request.session['session_slug'] = slug

    return redirect("/")


# we set the LoginSessionInfo active field to false to notify user has logged out
def logout_information(request,slug):
    try:
        login_obj = LoginSessionInfo.objects.filter(user = request.user, slug = slug)
        login_obj.update(active = False)
    except:
        pass

    return redirect("/accounts/logout")




