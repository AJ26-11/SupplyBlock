
from django.db import models

class CoffeeBeanBatch(models.Model):
    batch_id = models.CharField(max_length=255, unique=True)
    farm_name = models.CharField(max_length=255)
    origin_country = models.CharField(max_length=255)
    harvest_date = models.DateField()
    processing_details = models.TextField(blank=True)
    roasting_date = models.DateField(null=True, blank=True)
    packaging_details = models.TextField(blank=True)
    packaging_date = models.DateField(null=True, blank=True)
    is_shipped = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    current_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.batch_id
