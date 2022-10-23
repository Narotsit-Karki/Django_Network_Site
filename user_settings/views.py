from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from home.views import BaseView
from home.models import *
from .models import *
from django.contrib.auth.hashers import check_password

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
import os


countries = []
with open('home/countries.txt', 'r') as country:
    read = country.readline()
    while read:
        countries.append(read.strip('\n'))
        read = country.readline()

# Create your views here.

class BasicSettingsView(BaseView):

    def get(self, request):
        self.view
        return render(request, 'settings.html', self.view)

    def post(self, request):

        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']

        # change all info only when there are not username in other objects excluding yourself
        if not UserProfile.objects.exclude(username = request.user.username).filter(username = username).exists():
                request.user.username = username
                request.user.first_name = fname
                request.user.last_name = lname
                request.user.save()
                messages.success(request, 'Updated your profile successfully')
        else:
            messages.error(request, f'Username {username} already exists')

        return redirect('/settings/basic-settings')

class PasswordSettingsView(BaseView):

    def get(self,request):
        self.view
        return render(request , 'settings-password.html',self.view)


    def post(self,request):

        # changing the password
        cur_password_entered = request.POST['cur_password']
        new_password = request.POST['new_password']
        re_new_password = request.POST['re_new_password']

        #check current entered password with users previous password
        if check_password(cur_password_entered, request.user.password):
            if new_password == re_new_password:

                if new_password != cur_password_entered:
                    request.user.set_password(new_password)
                    request.user.save()

                    messages.success(request,'Password Updated Successfully')
                else:
                    messages.error(request,'Enter a new password different from previous one')
            else:
                messages.error(request,'Enter same password in new password fields')
        else:
            messages.error(request,'Your entered password does not match the current password')

        return redirect('/settings/password-settings')

class BillingSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['Billings'] = BillingMethod.objects.filter(user = request.user)
        return render(request, 'settings-billing-method.html', self.view)

class ContactSettingsView(BaseView):
    def get(self,request):
        self.view
        self.view['Countries'] = countries
        return render(request , 'settings-contact.html',self.view)


    def post(self,request):

        if request.method == 'POST':
            email = request.POST['email']
            phone = request.POST['phone']
            country_new = request.POST['country_new']
            city = request.POST['city']

            # update info only when current user email sent does not match other email excluding ourselve
            if not UserProfile.objects.exclude(username = request.user.username).filter(email = email).exists():
                request.user.email = email
                request.user.phone = phone
                request.user.country = country_new
                request.user.city = city
                request.user.save()

                messages.success(request, 'Updated your profile successfully')

            else:
                messages.error(request, f'Email {email} already exists')

            return redirect('/settings/contact-settings')



class FingerPrintSettingsView(BaseView):
    def get(self,request):
        self.view
        return render(request , 'settings-fingerprint.html',self.view)


class LocationSettingsView(BaseView):
    def get(self,request):
        self.view['Login_Sessions'] = LoginSessionInfo.objects.filter(user = request.user).order_by('-id')
        return render(request , 'settings-location.html',self.view)



class AddBillingView(BaseView):
    def get(self,request):
        self.view
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



@login_required
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

@login_required
def remove_billing(request , slug):
    try:
        remove_billing = BillingMethod.objects.filter(user = request.user , slug = slug)
        remove_billing.delete()
    except ObjectDoesNotExist:
        raise Http404

    return redirect('/settings/billing-settings')








