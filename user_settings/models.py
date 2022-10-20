from django.db import models
from django.contrib.auth.models import User

# Create your models here.
VENDOR = (
    ('paypal','Paypal'),
    ('visa','Visa')
)

class BillingMethod(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.CharField(max_length = 500)
    vendor = models.CharField(choices=VENDOR,max_length=400)
    card_number = models.IntegerField(max_length=500)
    cvc = models.IntegerField()
    card_owner = models.CharField(max_length=500)
    billing_address = models.CharField(max_length = 600)
    expiry_date = models.DateField()
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"< {self.user} : {self.vendor} >"
