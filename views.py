from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse

from datetime import timedelta

from dinner import models


def date_delta(days):
    """Return timedate object the number of days from/to current"""
    return timezone.now().date() + timedelta(days=days)

def index(request):
    context = {}
    context['random'] = models.Meal.objects.filter(
            created__gte = date_delta(-90)).values(
            'name', 'rating', 'foodtype__color', 'foodtype__name', 'common',
            ).order_by('?')[:3]
    context['random_names'] = [ x['name'] for x in context['random'] ]
    return render(request, 'base.html', context)

def overview(request, userid):
    max_rows = 10
    popular_days = 365
    context = {}
    context['random'] = models.Meal.objects.filter(owner=userid).values(
            'name', 'rating', 'foodtype__color', 'foodtype__name', 'common',
            ).order_by('?')[:3]
    context['random_names'] = [ x['name'] for x in context['random'] ]
    context['latest'] = models.Eaten.objects.filter(
            meal__owner=userid).values(
            'date', 'meal__name', 'meal__id', 'id', 'meal__common', 'meal__foodtype__color', 'meal__foodtype__name',
            ).order_by('-date')[:max_rows]
    context['popular'] = models.Meal.objects.filter(owner=userid,
            eaten__date__gte=date_delta(-popular_days)).values(
            'id','name', 'common', 'last_eaten', 'foodtype__color', 'foodtype__name').annotate(
            Count('eaten')).order_by(
            '-eaten__count','-last_eaten', 'name')[:max_rows]
    context['aging'] = models.Meal.objects.filter(
            common=True, owner=userid).values(
            'id', 'name', 'last_eaten', 'rating', 'foodtype__color', 'foodtype__name',
            ).order_by('last_eaten', '-rating', 'name')[:max_rows]
    context['cl'] = ['tan', 'green', 'cyan', 'orange', 'red']
    return render(request, 'dinner.html', context)

def meal_tip(request):
    html = []
    mealid = request.GET.get('id', '').rsplit('-',1)[-1]
    if mealid:
        meal = models.Meal.objects.get(id=mealid)

        if meal.foodtype.color:
            html.append('<div><div class="circle" style="background-color: #%s"></div> %s (food type)</div>' % (meal.foodtype.color, meal.foodtype.name))

        notes = []
        for e in models.Eaten.objects.filter(meal=mealid).order_by('-date', '-id')[:5]:
            if e.notes:
                notes.append("<b>[%s]</b> %s\n" % (e.date, e.notes))

        html.append(''.join(notes).replace('\n', '<br>'))

        if meal.notes:
            html.append('<hr>' + meal.notes)

    return HttpResponse(''.join(html))

