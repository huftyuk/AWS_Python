# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from polls.models import Observations
# Create your views here.

from django.utils import timezone

from django.http import HttpResponse 

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def test(request):
    return HttpResponse("test")	

class WeatherListView(ListView):
    model = Observations

    def get_context_data(self, **kwargs):
        context = super(WeatherListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
