from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    service = models.CharField(_("i.e screening"), max_length=100)
    
    def __str__(self):
        return self.service