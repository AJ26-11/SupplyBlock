from django.db import models


class Item(models.Model):
    item_id = models.CharField(max_length=255, unique=True)
    item_data = models.TextField()
    verified = models.BooleanField(default=False)
