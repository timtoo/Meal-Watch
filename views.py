from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, Form

from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from datetime import timedelta

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
def eaten(request):
    """Listen all eaten meals"""
    eaten = models.Eaten.objects.filter(
            meal__owner=request.user.id).values(
            'date', 'meal__name', 'meal__id', 'id', 'meal__common', 'meal__foodtype__color', 'meal__foodtype__name',
            ).order_by('-date')[:100]
    return render(request, 'eaten.html', { 'eaten': eaten })

@login_required(login_url=LOGIN_URL)
def meals(request, userid):
    """List all meals"""
    meals = models.Meal.objects.all()
    return render(request, 'meals.html', { 'meals': meals })

@login_required(login_url=LOGIN_URL)
def meal(request, meal_id):
    """Display info on a single meal"""
    return ""

@login_required(login_url=LOGIN_URL)
def foodtypes(request):
    """List food types"""
    return ''

@login_required(login_url=LOGIN_URL)
def add_eaten(request, userid):
    """Validate insert/update eaten record"""
    form = EatenForm()
    return render(request, 'eaten_add.html', {'form': form})

@login_required
def kse(request):
    """for testing"""
    return render(request, '_kse.html')


class EatenForm(ModelForm):
    class Meta:
        model = models.Eaten

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.form_action='add_eaten'
        self.helper.add_input(layout.Submit('submit', 'Submit'))
        self.helper.layout = layout.Layout(
            layout.Div(bootstrap.AppendedText('date', '<i class="icon-calendar"></i>')),
            'meal',
            'notes',)
        print self.helper.layout.fields

        super(EatenForm, self).__init__(*args, **kwargs)




