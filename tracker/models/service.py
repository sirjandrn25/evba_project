from django.db import models


class Service(models.Model):
    service_name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="service/")

    def __str__(self):
        return self.service_name