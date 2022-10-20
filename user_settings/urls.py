from django.urls import path ,include

from .views import *

urlpatterns = [
    path('basic-settings',BasicSettingsView.as_view(),name='basic-settings'),
    path('password-settings',PasswordSettingsView.as_view(),name = 'password-settings'),
    path('billing-settings',BillingSettingsView.as_view() , name = 'billing-settings'),
    path('contact-settings',ContactSettingsView.as_view() , name = 'contact-settings'),
    path('fingerprint-settings',FingerPrintSettingsView.as_view() , name = 'fingerprint-settings'),
    path('locations-settings',LocationSettingsView.as_view() , name = 'location-settings'),

    path('add-billing',AddBillingView.as_view() , name = 'add-billing'),
    path('set-primary-billing/<slug>',set_primary_billing, name = 'set-primary-billing'),
    path('remove-billing/<slug>',remove_billing, name = 'remove-billing')
]