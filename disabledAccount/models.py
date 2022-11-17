from django.db import models

# Create your models here.


class DiabledAccount(models.Model):
    account_name = models.EmailField(max_length=200, editable=False)
    date_joined = models.DateTimeField(editable=False)
    date_left = models.DateTimeField(editable=False)
    acc_type = models.CharField(max_length=20, editable=False)
    
    def __str__(self):
        return self.account_name
    