from django.db import models

class ServiceAccess(models.Model):
    service_name = models.CharField(max_length=100, default='nginx')
    access_allowed = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} - {'Allowed' if self.access_allowed else 'Denied'}"