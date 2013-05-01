from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, Form, TextInput, Textarea

from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from datetime import timedelta
import json

from dinner import models

LOGIN_URL = '/dinner/login'


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
    context['random_names'] = [ "%s %s" % (x['name'], x['foodtype__name']) for x in context['random'] ]
    context['random_names'].insert(0, 'recipe')
    context['form'] = EatenForm()
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

def overview_redirect(request):
    """Redirect to the logged in user's overview page"""
    return HttpResponseRedirect('/dinner/%s/' % request.user.id)

@login_required(login_url=LOGIN_URL)
def eaten(request, userid):
    """Listen all eaten meals"""
    eaten = models.Eaten.objects.filter(
            meal__owner=request.user.id).values(
            'date', 'meal__name', 'meal__id', 'id', 'meal__common', 'meal__foodtype__color', 'meal__foodtype__name',
            ).order_by('-date')[:500]

    eaten = models.Eaten.objects.eaten_with_count(ownerid=request.user.id)

    return render(request, 'eaten.html', { 'eaten': eaten })

@login_required(login_url=LOGIN_URL)
def meals(request, userid, foodtype=None):
    """List all meals"""
    title = 'All Meals'
    meals = models.Meal.objects.order_by('foodtype__name', 'name', 'id')
    if foodtype:
        meals = meals.filter(foodtype=foodtype)
        foodtype = models.FoodType.objects.get(id=foodtype)
        title = title + ' (%s)' % foodtype.name
    return render(request, 'meals.html', { 'meals': meals, 'foodtype': foodtype, 'title': title })

@login_required(login_url=LOGIN_URL)
def meal(request, userid, mealid):
    """Display info on a single meal"""
    meal = models.Meal.objects.get(id=mealid)
    eaten = models.Eaten.objects.filter(meal__id = mealid).order_by('-date','-id')
    attribs = []
    if meal.common:
        attribs.append("&#x2714; Common")
    if meal.freezable:
        attribs.append("&#x2714; Freezable")

    title = 'Meal: %s' % meal.name
    return render(request, 'meal.html', { 'meal': meal, 'eaten': eaten, 'title': title, 'attribs': ', '.join(attribs) })

@login_required(login_url=LOGIN_URL)
def foodtypes(request, userid):
    """List food types"""
    food = models.FoodType.objects.filter(owner=request.user.id).order_by('name', 'id').annotate(Count('meal'))
    return render(request, 'food_types.html', { 'food': food })

@login_required(login_url=LOGIN_URL)
def add_eaten(request, userid):
    """Validate insert/update eaten record"""
    if request.method == 'POST':
        form = EatenForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            meal = form.save()
            return HttpResponseRedirect('/dinner/%s/?added=%s-%s' % (request.user.id, meal.id, meal.meal.id))
    else:
        form = EatenForm()

    data = models.Meal.objects.values('id', 'name', 'foodtype__id', 'foodtype__name', 'foodtype__color')
    return render(request, 'eaten_add.html', {'form': form, 'meal_json': json.dumps(list(data))})

@login_required
def kse(request):
    """for testing"""
    return render(request, '_kse.html')


class EatenForm(ModelForm):

    class Meta:
        model = models.Eaten
        widgets = { 'meal': TextInput(attrs={'max_length': 120, 'style': 'width: 20em'}),
                    'notes': Textarea(attrs={'rows': 1, 'style': 'width: 22em', 'cols': 40})
                    }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.form_action='add_eaten'
        self.helper.add_input(layout.Submit('submit', 'Submit'))
        self.helper.layout = layout.Layout(
            layout.Div(bootstrap.AppendedText('date', '<i class="icon-calendar"></i>')),
            'meal',
            'notes',)
        print "y",self.helper.layout

        super(EatenForm, self).__init__(*args, **kwargs)




