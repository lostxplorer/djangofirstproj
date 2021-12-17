import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Questions(models.Model):
    Q_text = models.CharField(max_length=200)
    p_date = models.DateTimeField('Date published')
    
    def __str__(self):
        return self.Q_text
    
    def was_pub_recently(self):
        return timezone.now() >= self.p_date >= timezone.now() - datetime.timedelta(days=1) 
    
class Choice(models.Model):
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)
    C_text= models.CharField(max_length=100)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.C_text