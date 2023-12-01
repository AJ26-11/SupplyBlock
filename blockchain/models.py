
from django.db import models


class Batch(models.Model):
    batch_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.batch_id

