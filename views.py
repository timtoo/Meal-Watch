from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count

from datetime import timedelta

from dinner import models


def date_delta(days):
    """Return timedate object the number of days from/to current"""
    return timezone.now().date() + timedelta(days=days)


def index(request):
    max_rows = 10
    popular_days = 365
    context = {}
    context['random'] = models.Meal.objects.select_related().order_by('?')[:3]
    context['latest'] = models.Eaten.objects.select_related().order_by('-date')[:max_rows]
    context['popular'] = models.Eaten.objects.filter(
            date__gte=date_delta(-popular_days)).values(
            'meal_id','meal__name', 'meal__common').annotate(
            Count('meal')).order_by(
            '-meal__count','-date', 'meal__name')[:max_rows]
    context['aging'] = models.Meal.objects.filter(common=True).select_related(
            ).order_by('last_eaten', '-rating', 'name')[:max_rows]
    return render(request, 'dinner.html', context)


