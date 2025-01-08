from django.core.exceptions import ValidationError # type: ignore
from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Resources(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    total_quantity = models.IntegerField(null=False, blank=False)
    available_quantity = models.IntegerField()

    def clean(self):
        if self.total_quantity < 0:
            raise ValidationError({'total_quantity': 'Total quantity cannot be less than 0.'})
        if self.available_quantity < 0:
            raise ValidationError({'available_quantity': 'Available quantity cannot be less than 0.'})

    def __str__(self):
        return f"{self.id}, {self.name}, {self.description}, {self.total_quantity}, {self.available_quantity}"
    
class Bookings(models.Model):
    id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=False, blank=False)
    resource = models.ForeignKey(Resources, on_delete=models.CASCADE, related_name='bookings', null=False, blank=False)
    purchase_quantity = models.IntegerField(null=False, blank=False)
    booking_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.purchase_quantity > self.resource.available_quantity:
            raise ValidationError({
                'purchase_quantity': 'Purchase quantity cannot exceed the available quantity of the resource.'
            })
    
    def __str__(self):
        return f"{self.id}, {self.user}, {self.resource}, {self.purchase_quantity}, {self.booking_date}"
