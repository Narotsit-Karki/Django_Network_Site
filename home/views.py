import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

import os
# Create your views here.

from django.views.generic.base import View
from functools import reduce
import operator
from django.db.models import Q
from notifications.signals import notify
from post_app.models import *

notification_messsage = {
    'friend-request-send': 'sent you a friend request',
    'friend-request-accept': 'accepted your friend request',
    'following-you': 'started following you',
    'new-post': 'uploaded a new post check it out',
}

# a function just to get all countries as a list
countries = []
with open('home/countries.txt', 'r') as country:
    read = country.readline()
    while read:
        countries.append(read.strip('\n'))
        read = country.readline()


class BaseView(LoginRequiredMixin, View):
    view = dict()
    login_url = '/login'
    redirect_field_name = '/login-info'


# main homepage view
class HomeView(BaseView):
    def get_required_info(self,request):
        self.view['Saved_Posts'] = SavedPost.objects.filter(user = request.user,is_saved = True).count()

    def get(self, request):
        self.view
        self.get_required_info(request)
        return render(request, 'index.html', self.view)


# view to set all users notificatins as marked
@login_required
def mark_as_read_delete(request):
    if request.method == 'GET':
        if request.GET['mark'] == 'read':
            request.user.notifications.mark_all_as_read()
        elif request.GET['mark'] == 'delete':
            request.user.notifications.all().delete()
        else:
            pass

        return HttpResponse('marked')
    else:
        return HttpResponse('invalid request')

class SignUpView(View):
    def post(self, request, *args, **kwargs):
        self.add_new_user(request)
        messages.success(request, 'Signed Up Successfully')
        return redirect('/login')

    def add_new_user(self, request):
        fname, lname = request.POST['fname'], request.POST['lname']
        username = request.POST['username']
        email, phone = request.POST['email'], request.POST['phone']
        gender = request.POST['gender']
        country, city = request.POST['country'], request.POST['city']

        dob = request.POST['dob']
        password, confirm_password = request.POST['password'], request.POST['password']

        if password == confirm_password:
            if not UserProfile.objects.filter(username=username, email=email).exists():
                profile_user = UserProfile.objects.create_user(
                    username=username,
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    city=city,
                    country=country,
                    dob=dob,
                    gender=gender,
                    phone=phone,
                    password=password
                )
                profile_user.save()

            else:
                messages.error(request, 'username or email already exists')
                return redirect('/signup')
        else:
            messages.error(request, 'Enter Same password on both fields')
            return redirect('/signup')

    def get(self, request):

        signup_view = {}
        today = datetime.datetime.now()
        max_date = today.strftime("%Y-%m-%d")
        signup_view['max_date'] = max_date  # max date for the date input
        signup_view['min_date'] = '1900-01-01'  # min date for the date input
        signup_view['Countries'] = countries  # a list of countries to show is the select field for country

        return render(request, 'sign-up.html', signup_view)


class ProfileView(BaseView):

    def get_user(self, request, username):
        user_obj = UserProfile.objects.get(username=username)

        following, friend, sent_friend_request = False, False, False

        # check if current user is following viewed user
        if UserProfile.objects.filter(username=request.user.username, user_followers__in=[user_obj]).exists():
            following = True
        # check to see if current user is in viewed users friends list
        if UserProfile.objects.filter(username=user_obj.username, user_friends__in=[request.user]).exists():
            friend = True
        # check to see if current user has sent friend request to the viewed user
        elif FriendRequest.objects.filter(from_user=request.user, to_user=user_obj).exists():
            sent_friend_request = True

        self.view['User_Profile'] = user_obj
        self.view['Following'] = following
        self.view['Friend'] = friend
        self.view['Friend_Request_Sent'] = sent_friend_request
        # get user posts
        self.view['User_Posts'] = UserPost.objects.filter(user=self.view['User_Profile']).order_by('-created_at')

        # get hidden posts by the user
        self.view['Hidden_Posts'] = HiddenPost.objects.filter(post__in = [post for post in self.view['User_Posts']],user = request.user, is_hidden = True,)
        h_post_id = [h_post.post.id for h_post in self.view['Hidden_Posts']]
        self.view['Hidden_Posts'] = UserPost.objects.filter(id__in = h_post_id)
        print(self.view['Hidden_Posts'])

    def get(self, request, username):
        self.view
        self.get_user(request, username)
        return render(request, 'profile.html', self.view)




class AboutView(ProfileView):
    def get(self, request, username):
        self.view
        self.get_user(request, username)
        return render(request, 'about.html', self.view)


class FriendView(ProfileView):
    def get(self, request, username):
        self.get_user(request, username)
        return render(request, 'friends.html', self.view)




class SavedView(ProfileView):

    def get(self, request, username):
        self.view['Saved_Posts'] = SavedPost.objects.filter(user=request.user, is_saved=True)
        s_post_id = [h_post.post.id for h_post in self.view['Saved_Posts']]
        self.view['Saved_Posts'] = UserPost.objects.filter(id__in=s_post_id)
        self.view['User_Profile'] = request.user
        return render(request, 'saved.html', self.view)


# error 404
def error_404(request, exception):
    return render(request, '404.html')


@login_required
def follow_unfollow_user(request):
    if request.method == "GET":
        username = request.GET['username']
        follow_user = UserProfile.objects.get(username=username)

        # if already followed unfollow else follow
        if UserProfile.objects.filter(username=request.user.username, user_followers__in=[follow_user]).exists():
            request.user.following.remove(follow_user)
        else:
            request.user.user_followers.add(follow_user)
            notify.send(sender=request.user,
                        recipient=follow_user,
                        verb='bxs-group',
                        description=notification_messsage['following-you']
                        )

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
        profiles = UserProfile.objects.exclude(username=request.user.username).filter(
            reduce(operator.and_, (Q(username__icontains=x) for x in keyword)))

        # get current users friend list to see if searched user is present or not
        user_friend_requests = FriendRequest.objects.filter(to_user__in=list(profiles), from_user=request.user)

        if user_friend_requests.count() == 0:
            self.view['User_Friend_Requests'] = user_friend_requests
        else:
            self.view['User_Friend_Requests'] = UserProfile.objects.filter(
                reduce(operator.and_, (Q(username=f.to_user.username) for f in user_friend_requests)))

        # get searched users friend requests to see if current user is present there or not
        searched_user_friend_requests = FriendRequest.objects.filter(from_user__in=list(profiles), to_user=request.user)

        if searched_user_friend_requests.count() == 0:
            self.view['Searched_User_Friend_Requests'] = searched_user_friend_requests
        else:
            self.view['Searched_User_Friend_Requests'] = UserProfile.objects.filter(
                reduce(operator.and_, (Q(username=f.from_user.username) for f in searched_user_friend_requests)))

        self.view['Searched_Users'] = profiles

    def get(self, request):
        search = request.GET['search']

        # getting User Friends as  query set for searching purpose
        self.view['User_Friends'] = request.user.user_friends.get_queryset()
        self.search_algorithm(query=search, request=request)
        return render(request, 'search.html', self.view)


@login_required
def send_friend_request_or_remove(request):
    if request.method == "GET":
        username = request.GET['addfriend_username']
        from_user = request.user
        to_user = UserProfile.objects.get_object_or_404(username=username)

        # check to see if not both users are friends already
        if UserProfile.objects.filter(username=from_user.username,
                                      user_friends__in=[to_user]).exists() or UserProfile.objects.filter(
                username=to_user.username, friends__in=[from_user]).exists():
            return redirect(request.META.get('HTTP_REFERER'))

        # send friend request
        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

        # request was already sent now we delete it
        if not created:
            friend_request.delete()
        else:
            notify.send(sender=from_user, recipient=to_user, verb='Message',
                        description=notification_messsage['friend-request-send'])

    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def accept_friend_request(request):
    if request.method == 'GET':
        try:
            from_username = request.GET['u_name']
            from_user = UserProfile.objects.get(username=from_username)
            friend_request = FriendRequest.objects.get(from_user=from_user, to_user=request.user)

            # add both of users as friends to each other
            friend_request.from_user.user_friends.add(friend_request.to_user)
            friend_request.to_user.user_friends.add(friend_request.from_user)

            # also add both of them as followers of each other
            friend_request.from_user.user_followers.add(friend_request.to_user)
            friend_request.to_user.user_followers.add(friend_request.from_user)

            notify.send(sender=friend_request.to_user,
                        recipient=friend_request.from_user,
                        verb='Message',
                        description=notification_messsage['friend-request-accept']
                        )
            # delete the friend request after being accepted
            friend_request.delete()

        except Exception:  # for any concurrency problems
            pass

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def store_login_info(request):
    if request.user_agent.is_mobile:
        device = 'mobile'
    elif request.user_agent.is_pc:
        device = 'pc'
    elif request.user_agent.is_tablet:
        device = 'tablet'
    elif request.user_agent.is_bot:
        device = 'PC'

    slug = os.urandom(8).hex()

    login_object = LoginSessionInfo.objects.create(
        slug=slug,
        user=request.user,
        os=request.user_agent.os.family,
        device=device,
        device_type=request.user_agent.device.family,
        browser=request.user_agent.browser.family,
        active=True,
    )

    login_object.save()

    # save in the slug so that we can set the user active to not active if the user logs out
    request.session['session_slug'] = slug

    return redirect("/")


# we set the LoginSessionInfo active field to false to notify user has logged out
def logout_information(request, slug):
    try:
        login_obj = LoginSessionInfo.objects.filter(user=request.user, slug=slug)
        login_obj.update(active=False)
    except:
        pass

    return redirect("/accounts/logout")
