from django.db import models


# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_package = models.CharField(max_length=100)
    service_tax = models.DecimalField(max_digits=5, decimal_places=2)
    service_image = models.ImageField(upload_to='services/')
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.service_name



class Subscription(models.Model):
     order_id = models.CharField(max_length=100)
     payment_id = models.CharField(max_length=100)
     status = models.CharField(max_length=50)  # SUCCESS or FAILURE
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.order_id
