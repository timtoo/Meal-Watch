from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from datetime import timedelta

from dinner import models


def date_delta(days):
    """Return timedate object the number of days from/to current"""
    return timezone.now().date() + timedelta(days=days)

def index(request):
    context = {}
    context['random'] = models.Meal.objects.filter(
            created__gte = date_delta(-90)).select_related(
            ).order_by('?')[:3]
    context['random_names'] = [ x.name for x in context['random'] ]
    return render(request, 'base.html', context)

def overview(request, userid):
    max_rows = 10
    popular_days = 365
    context = {}
    context['random'] = models.Meal.objects.filter(owner=userid).select_related().order_by('?')[:3]
    context['random_names'] = [ x.name for x in context['random'] ]
    context['latest'] = models.Eaten.objects.filter(meal__owner=userid).select_related().order_by('-date')[:max_rows]
    context['popular'] = models.Meal.objects.filter(owner=userid,
            eaten__date__gte=date_delta(-popular_days)).values(
            'id','name', 'common', 'last_eaten').annotate(
            Count('eaten')).order_by(
            '-eaten__count','-last_eaten', 'name')[:max_rows]
    context['aging'] = models.Meal.objects.filter(common=True, owner=userid).select_related(
            ).order_by('last_eaten', '-rating', 'name')[:max_rows]
    return render(request, 'dinner.html', context)


