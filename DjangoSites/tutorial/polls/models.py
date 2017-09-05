# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published') 

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Observations(models.Model):
    NObs = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField() 
	LocationID = models.IntegerField()
	Temperature = models.FloatField(null=True)
	Pressure = models.SmallIntegerField(null=True)
	Screen_Relative_Humidity = models.FloatField(null=True)
	Wind_Speed = models.SmallIntegerField(null=True)
	Visibility = models.SmallIntegerField(null=True)
	Dew_Point = models.FloatField(null=True)
	Pressure_Tendency = models.CharField(max_length=5, null=True)
	Weather_Type = models.SmallIntegerField(null=True)
	Wind_Direction = models.CharField(max_length=3, null=True)
	Wind_Gust = models.SmallIntegerField(null=True)
