from django.shortcuts import render, redirect
from home.views import BaseView
from home.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
import os
from .models import *

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
        self.view['Billings'] = BillingMethod.objects.filter(user = request.user)

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

    def post(self,request):

        card_number = request.POST['card_number']
        cvc = request.POST['cvc']
        expiry_date = request.POST['exp_date']
        owner = request.POST['owner']
        vendor = request.POST['vendor']
        billing_address = request.POST['address']
        slug = os.urandom(8).hex()

        billing_obj = BillingMethod.objects.create(
            user = request.user,
            card_number = card_number,
            cvc = cvc,
            expiry_date = expiry_date,
            card_owner = owner,
            vendor = vendor ,
            billing_address = billing_address,
            slug = slug,
            is_primary = False
        )
        billing_obj.save()

        return redirect('/settings/billing-settings')

def set_primary_billing(request , slug):
    try:
        selected_non_primary_billing = BillingMethod.objects.filter(slug = slug , user = request.user)
        if BillingMethod.objects.filter(user = request.user , is_primary = True).exists():
            current_primary_billing = BillingMethod.objects.filter(user = request.user , is_primary = True)
            current_primary_billing.update(is_primary = False)
            selected_non_primary_billing.update(is_primary = True)
        else:
            selected_non_primary_billing.update(is_primary = True)

    except ObjectDoesNotExist:
        raise Http404

    return redirect('/settings/billing-settings')

def remove_billing(request , slug):
    try:
        remove_billing = BillingMethod.objects.filter(user = request.user , slug = slug)
        remove_billing.delete()
    except ObjectDoesNotExist:
        raise Http404

    return redirect('/settings/billing-settings')








