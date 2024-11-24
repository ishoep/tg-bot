from django.db import models

class UserRegistration(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    event_id = models.CharField(max_length=100)
    date = models.DateTimeField()
    hash_id = models.CharField(max_length=100)
    hash_name = models.CharField(max_length=100)
    source_id = models.CharField(max_length=100)
    source_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    sub1 = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_id
