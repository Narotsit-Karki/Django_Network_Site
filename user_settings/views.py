from django.shortcuts import render, redirect
from home.views import BaseView
from home.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages


# Create your views here.

class BasicSettingsView(BaseView):

    def get(self, request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request, 'settings.html', self.view)

    def post(self, request):

        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']

        if not User.objects.filter(username = username).exists() and not Profile.objects.filter(username=username):

            try:
                auth_user = User.objects.filter(username=request.user.username)
                auth_user.update(username = username, first_name=fname, last_name=lname)

                # updating in profile model
                user_profile = Profile.objects.filter(user=request.user, username=request.user.username)
                user_profile.update(username=username, fname=fname, lname=lname)

                messages.success(request, 'Updated your profile successfully')

            except ObjectDoesNotExist:
                raise Http404
        else:
            messages.error(request, f'Username {username} already exists')

        return redirect('/settings/basic')

class PasswordSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request , 'settings-password.html',self.view)

class BillingSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request, 'settings-billing-method.html', self.view)

class ContactSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request , 'settings-contact.html',self.view)

class FingerPrintSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request , 'settings-fingerprint.html',self.view)

class LocationSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request , 'settings-location.html',self.view)


class AddBillingView(BaseView):
    def get(self,request):
        self.view
        self.view['auth_user'] = self.get_user(request)
        return render(request , 'add_billing_method.html',self.view)