from django.db import models


class KVStore(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"

