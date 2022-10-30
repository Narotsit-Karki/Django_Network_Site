import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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
    login_url = '/accounts/login'
    redirect_field_name = '/login-info'


# main homepage view
class HomeView(BaseView):
    def get_required_info(self, request):
        self.view['Saved_Posts'] = SavedPost.objects.filter(user=request.user, is_saved=True).count()
        users_post = [follower for follower in request.user.user_followers.all()]
        users_post.append(request.user)
        self.view['User_Posts'] = UserPost.objects.filter(user__in = users_post ).order_by('-created_at')

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


class ProfileView(BaseView):

    def get_user(self, request, username):
        user_obj = get_object_or_404(UserProfile,username=username)

        following, friend, sent_friend_request, friend_request_got = False, False, False, False

        # check if current user is following viewed user
        if UserProfile.objects.filter(username=request.user.username, user_followers__in=[user_obj]).exists():
            following = True
        # check to see if current user is in viewed users friends list
        if UserProfile.objects.filter(username=user_obj.username, user_friends__in=[request.user]).exists():
            friend = True
        # check to see if current user has sent friend request to the viewed user
        elif FriendRequest.objects.filter(from_user=request.user, to_user=user_obj).exists():
            sent_friend_request = True

        elif FriendRequest.objects.filter(from_user= user_obj, to_user= request.user).exists():
            friend_request_got = True

        self.view['User_Profile'] = user_obj
        self.view['Following'] = following
        self.view['Friend'] = friend
        self.view['Friend_Request_Sent'] = sent_friend_request
        self.view['Friend_Request_Got'] = friend_request_got
        # get user posts
        self.view['User_Posts'] = UserPost.objects.filter(user=self.view['User_Profile']).order_by('-created_at')

        # get hidden posts by the user
        self.view['Hidden_Posts'] = HiddenPost.objects.filter(post__in=[post for post in self.view['User_Posts']],
                                                              user=request.user, is_hidden=True, )
        h_post_id = [h_post.post.id for h_post in self.view['Hidden_Posts']]
        self.view['Hidden_Posts'] = UserPost.objects.filter(id__in=h_post_id)


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


class FindFriendView(ProfileView):
    def friend_suggestion(self,request):

        if request.user.user_friends.count() > 0:
            friend_suggestion_list = []
            friends = request.user.user_friends.all()
            for friend in friends:
                for f_friend in friend.user_friends.all():
                    if f_friend != request.user and f_friend not in request.user.user_friends.all():
                        friend_suggestion_list.append(f_friend)

            self.view['Friend_Suggestions'] = friend_suggestion_list
        else:
            self.view['Friend_Suggestions'] = UserProfile.objects.exclude(username = request.user.username).filter(city__icontains = request.user.city,country__icontains = request.user.country)

    def get(self, request):
        self.get_user(request, request.user.username)
        self.friend_suggestion(request)
        return render(request, 'find-friends.html', self.view)


class PhotosView(ProfileView):
    def get(self, request, username):
        self.get_user(request, username)
        self.view['User_Photos'] = UserImage.objects.filter(user=request.user).order_by('-date_uploaded')
        return render(request, 'photos.html', self.view)


class SignUpView(View):
    def post(self, request, *args, **kwargs):
        self.add_new_user(request)
        messages.success(request, 'Signed Up Successfully')
        return redirect('/accounts/login')

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


# stores users saved posts
class SavedView(ProfileView):

    def get(self, request, username):
        self.view['Saved_Posts'] = SavedPost.objects.filter(user=request.user, is_saved=True)
        s_post_id = [h_post.post.id for h_post in self.view['Saved_Posts']]
        self.view['Saved_Posts'] = UserPost.objects.filter(id__in=s_post_id)
        self.view['User_Profile'] = request.user
        return render(request, 'saved.html', self.view)









class SearchView(BaseView):
    # removing any blank spaces and only getting words
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

        self.view['Searched_Users'] = profiles

    def get(self, request):
        search = request.GET['search']

        self.search_algorithm(query=search, request=request)
        return render(request, 'search.html', self.view)

@login_required
def follow_unfollow_user(request):
    if request.method == "POST":
        username = request.POST['u_name']
        follow_user = UserProfile.objects.get(username=username)

        # if already followed unfollow else follow
        if follow_user in request.user.user_followers.all():
            request.user.user_followers.remove(follow_user)
        else:
            request.user.user_followers.add(follow_user)
            notify.send(sender=request.user,
                        recipient=follow_user,
                        verb='bxs-group',
                        description=notification_messsage['following-you']
                        )

        request.user.save()

        return redirect(f'/profile/{username}')

@login_required
def send_friend_request_or_remove(request):
    if request.method == "POST":
        username = request.POST['u_name']
        from_user = request.user
        to_user = get_object_or_404(UserProfile, username=username)

        # check to see if not both users are friends already
        if UserProfile.objects.filter(username=from_user.username,
                                      user_friends__in=[to_user]).exists() or UserProfile.objects.filter(
            username=to_user.username, user_friends__in=[from_user]).exists():
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
    if request.method == 'POST':
        try:
            from_username = request.POST['u_name']
            from_user = get_object_or_404(UserProfile, username=from_username)
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

        except Exception:
            pass

    return redirect(request.META.get("HTTP_REFERER"))

@login_required
def unfriend(request):
    if request.method == "POST":
        user_name = request.POST['u_name']
        unfriend_user = get_object_or_404(UserProfile, username=user_name)
        unfriend_user.user_friends.remove(request.user)
        unfriend_user.user_followers.remove(request.user)
        request.user.user_friends.remove(unfriend_user)
        request.user.user_followers.remove(unfriend_user)

    return redirect(request.META['HTTP_REFERER'])



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





# for updating user background image
@login_required
def update_background(request, username):
    if request.method == "POST" and request.user.username == username:
        user_obj = get_object_or_404(UserProfile,username=username)
        background_image = request.FILES.get('background_image')
        if os.path.exists(user_obj.background_pic.path):
            os.remove(user_obj.background_pic.path)

        user_obj.background_pic = background_image
        user_obj.save()

    return redirect(request.META['HTTP_REFERER'])


# for updating user profile picture
@login_required
def update_profile_pic(request, username):
    if request.method == "POST" and request.user.username == username:
        user_obj = get_object_or_404(UserProfile,username=username)
        profile_image = request.FILES.get('profile_image')
        if os.path.exists(user_obj.profile_pic.path):
            os.remove(user_obj.profile_pic.path)

        user_obj.profile_pic = profile_image
        user_obj.save()

        if request.user.gender == "male":
            pronoun = 'his'
        elif request.user.gender == "female":
            pronoun = 'her'
        else:
            pronoun = 'the'

        # create a new post for updated profile
        profile_update_post = UserPost.objects.create(
            user=request.user,
            slug=os.urandom(6).hex(),
            post_image=profile_image,
            snap_message=f"updated {pronoun} profile picture"
        )
        profile_update_post.save()

        # notify_all followers of user
        notify.send(sender=request.user, recipient=request.user.user_followers.all(), verb='bxs-group',
                    description=f"updated {pronoun} profile picture")

    return redirect(request.META['HTTP_REFERER'])

# error 404
def error_404(request, exception):
    return render(request, '404.html')
#error 503
def error_503(request,exception):
    return render(request,'503.html')
#error 403
def error_403(request,exception):
    return render(request,'403.html')