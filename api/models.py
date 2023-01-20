from django.db import models

# Create your models here.

class Results(models.Model):
    stockid = models.AutoField(primary_key=True)
    stockname = models.CharField(max_length=50)
    stratergy = models.CharField(default=None, max_length=100)
    fullname = models.CharField(max_length=100)
    entry_price = models.FloatField(default=None)
    exit_price = models.FloatField(default=None)
    entry_date = models.DateField(default=None)
    exit_date = models.DateField(auto_now=True)
    profit = models.FloatField(default=None)  
    percentage = models.FloatField(default=None)

    def __str__(self):
        return self.title


class Todays_pick(models.Model):
    stockid = models.AutoField(primary_key=True)
    stockname = models.CharField(max_length=50)
    fullname = models.CharField(max_length=100)
    entry_price = models.FloatField(default=None)
    exit_price = models.FloatField(default=None)
    time_frame = models.DateField(max_length=50)

    def __str__(self):
        return self.title


