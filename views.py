from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm, Form, TextInput, Textarea, HiddenInput
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
    context['userid'] = userid
    return render(request, 'dinner.html', context)

def meal_tip(request, userid):
    html = []
    mealid = request.GET.get('id', '').rsplit('-',1)[-1]
    if mealid:
        meal = models.Meal.objects.get(id=mealid, owner=userid)

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
    title = "Meals Eaten"

    return render(request, 'eaten.html', { 'eaten': eaten, 'title': title })

@login_required(login_url=LOGIN_URL)
def meals(request, userid, foodtype=None):
    """List all meals"""
    title = 'All Meals'
    meals = models.Meal.objects.order_by('foodtype__name', 'name', 'id').annotate(Count('eaten'))
    if foodtype:
        meals = meals.filter(foodtype=foodtype)
        foodtype = models.FoodType.objects.get(id=foodtype)
        title = title + ' (%s)' % foodtype.name
    return render(request, 'meals.html', { 'meals': meals, 'foodtype': foodtype, 'title': title })

@login_required(login_url=LOGIN_URL)
def meal(request, userid, mealid):
    """Display info on a single meal"""
    try:
        meal = models.Meal.objects.get(id=mealid, owner=request.user.id)
    except models.Meal.DoesNotExist:
        messages.add_message(request, messages.ERROR, "Meal %s does not exist for user %s." % (mealid, userid))
        return HttpResponseRedirect('/dinner/%s/' % (request.user.id,))


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
def eaten_edit(request, userid, eatenid=None):
    """Validate insert/update eaten record"""
    instance = None

    if eatenid:

        # verify ownership of record
        try:
            instance = models.Eaten.objects.owned(eatenid, request.user.id)
        except models.Eaten.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No such eaten meal: %s' % eatenid)
            return HttpResponseRedirect('/dinner/%s/' % (request.user.id,))

    if request.method == 'POST':
        if request.POST.get('remove') == '1':
            messages.add_message(request, messages.WARNING, 'Deleted eaten meal %s: %s' % (instance.id, instance.meal.name))
            url = '/dinner/%s/meal/%s' % (request.user.id, instance.meal.id,)
            instance.delete()
            return HttpResponseRedirect(url)
        else:
            form = EatenForm(request.POST, instance=instance)
            if form.is_valid():
                meal = form.save()
                messages.add_message(request, messages.INFO, 'Updated eaten meal %s: %s' % (meal.id, meal.meal.name))
                return HttpResponseRedirect('/dinner/%s/meal/%s' % (request.user.id, meal.meal.id,))
    else:
        form = EatenForm(instance=instance)

    # delete button if editing
    if eatenid:
        form.helper.layout.fields[-1].fields.append(extraButton('delete', 'delete', 'color: red'))
        form.helper.form_action = '/dinner/%s/eaten/%s/edit' % (request.user.id, instance.id)
        title = "Modify an eaten meal"
    else:
        form.helper.form_action = '/dinner/%s/eaten/new' % (request.user.id,)
        title = "Record an eaten meal"

    form.fields['meal'].queryset = models.Meal.objects.filter(owner=request.user.id).order_by('name', 'id')
    data = form.fields['meal'].queryset.values('id', 'name', 'foodtype__id', 'foodtype__name', 'foodtype__color')

    return render(request, 'eaten_add.html', {'form': form, 'title': title, 'select_json': json.dumps(list(data)), 'instance': instance})

@login_required(login_url=LOGIN_URL)
def meal_edit(request, userid, pid=None):
    """Validate insert/update eaten record"""
    instance = None

    if pid:
        # verify ownership of record
        try:
            instance = models.Meal.objects.get(owner=request.user.id, id=pid)
        except models.Eaten.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No such meal: %s' % pid)
            return HttpResponseRedirect('/dinner/%s/' % (request.user.id,))

    if request.method == 'POST':
        if request.POST.get('remove') == '1':
            messages.add_message(request, messages.WARNING, 'Deleted meal %s: %s' % (pid, instance.name))
            url = '/dinner/%s/meals' % (request.user.id,)
            instance.delete()
            return HttpResponseRedirect(url)
        else:
            data = request.POST.copy()
            if instance:
                # don't allow changing owner
                data['owner'] = instance.owner.id
            else:
                # force owner to current user
                data['owner'] = request.user.id

            form = MealForm(data, instance=instance)

            if form.is_valid():
                meal = form.save()
                messages.add_message(request, messages.INFO, 'Updated meal %s: %s' % (pid, meal.name))
                return HttpResponseRedirect('/dinner/%s/meal/%s?updated=%s' % (request.user.id, meal.id, meal.id))
    else:
        form = MealForm(instance=instance)

    # delete button if editing
    if pid:
        form.helper.form_action = '/dinner/%s/meal/%s/edit' % (request.user.id, instance.id)
        form.helper.layout.fields[-1].fields.append(extraButton('delete', 'delete', 'color: red'))
        title = 'Modify a meal record'
    else:
        form.helper.form_action = '/dinner/%s/meal/new' % (request.user.id,)
        title = "Create a meal record"

    form.fields['foodtype'].queryset = models.FoodType.objects.filter(owner=request.user.id).order_by('name', 'id')
    data = form.fields['foodtype'].queryset.values('id', 'name', 'color')

    return render(request, 'meal_edit.html', {
            'form': form, 'title': title,
            'select_json': json.dumps(list(data)),
            'instance': instance,
            'confirm_remove': 'Really remove (and any attached eaten meals)?',
            })

@login_required(login_url=LOGIN_URL)
def foodtype_edit(request, userid, pid=None):
    """Validate insert/update eaten record"""
    instance = None

    if pid:
        # verify ownership of record
        try:
            instance = models.FoodType.objects.get(owner=request.user.id, id=pid)
        except models.Eaten.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No such food type: %s' % pid)
            return HttpResponseRedirect('/dinner/%s/foodtypes' % (request.user.id,))

    if request.method == 'POST':
        if request.POST.get('remove') == '1':
            messages.add_message(request, messages.WARNING, 'Deleted food type %s: %s' % (pid, instance.name))
            url = '/dinner/%s/foodtypes' % (request.user.id,)
            instance.delete()
            return HttpResponseRedirect(url)
        else:
            data = request.POST.copy()
            if instance:
                # don't allow changing owner
                data['owner'] = instance.owner.id
            else:
                # force owner to current user
                data['owner'] = request.user.id

            form = FoodTypeForm(data, instance=instance)

            if form.is_valid():
                record = form.save()
                messages.add_message(request, messages.INFO, 'Updated food type %s: %s' % (pid, record.name))
                return HttpResponseRedirect('/dinner/%s/foodtypes' % (request.user.id,))
    else:
        form = FoodTypeForm(instance=instance)

    # delete button if editing
    if pid:
        form.helper.form_action = '/dinner/%s/foodtype/%s/edit' % (request.user.id, instance.id)
        form.helper.layout.fields[-1].fields.append(extraButton('delete', 'delete', 'color: red'))
        title = 'Modify a food type record'
    else:
        form.helper.form_action = '/dinner/%s/foodtype/new' % (request.user.id,)
        title = "Create a food type record"

    data = []
    return render(request, 'meal_edit.html', {
            'form': form, 'title': title,
            'select_json': json.dumps(list(data)),
            'instance': instance,
            'confirm_remove': 'Really remove (AND ALL ATTACHED MEALS)?',
            })

@login_required(login_url=LOGIN_URL)
def kse(request):
    """for testing"""
    return render(request, '_kse.html')


def extraButton(idstr, label, style=None):
    template = ' &nbsp;&nbsp;&nbsp; <a href="#" id="button-id-%s" style="vertical-align: middle; margin-left: 2em">%s</a>'
    if style:
        template = template.replace('style="', 'style="%s; ' % style)
    return layout.HTML(template % (idstr, label))

class EatenForm(ModelForm):

    class Meta:
        model = models.Eaten
        fields = [ 'meal', 'notes', 'date' ]
        widgets = { 'meal': TextInput(attrs={'max_length': 120, 'style': 'width: 20em'}),
                    'notes': Textarea(attrs={'rows': 1, 'style': 'width: 22em', 'cols': 40})
                    }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'eaten-edit-form'
        self.helper.form_class='form-horizontal'
        self.helper.form_action=''
        #self.helper.add_input(layout.Submit('submit', 'Submit'))
        self.helper.layout = layout.Layout(
            layout.Div(bootstrap.AppendedText('date', '<i class="icon-calendar"></i>')),
            'meal',
            'notes',
            layout.ButtonHolder(layout.Submit('submit_', 'Submit', css_class="controls"),
                    extraButton('cancel_', 'cancel'))
        )

        super(EatenForm, self).__init__(*args, **kwargs)

class MealForm(ModelForm):

    class Meta:
        model = models.Meal
        fields = [ 'name', 'foodtype', 'notes', 'prep_mins', 'common', 'freezable', 'rating', 'owner']
        widgets = { 'notes': Textarea(attrs={'rows': 1, 'style': 'width: 22em', 'cols': 40}),
                    'owner': HiddenInput() }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'meal-edit-form'
        self.helper.form_class='form-horizontal'
        self.helper.form_action=''
        self.helper.layout = layout.Layout(
            'name',
            'foodtype',
            'notes',
            'prep_mins',
            'common',
            'freezable',
            'rating',
            layout.ButtonHolder(layout.Submit('submit_', 'Submit', css_class="controls"),
                    extraButton('cancel_', 'cancel'))
        )

        super(MealForm, self).__init__(*args, **kwargs)

class FoodTypeForm(ModelForm):

    class Meta:
        model = models.FoodType
        fields = [ 'name', 'color', 'owner']
        widgets = { 'owner': HiddenInput() }

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'foodtype-edit-form'
        self.helper.form_class='form-horizontal'
        self.helper.form_action=''
        self.helper.layout = layout.Layout(
            'name',
            'color',
            layout.ButtonHolder(layout.Submit('submit_', 'Submit', css_class="controls"),
                    extraButton('cancel_', 'cancel'))
        )

        super(FoodTypeForm, self).__init__(*args, **kwargs)



# XXX probably should disable this for production...
def auth4tim4testing(request):
    """instant authenticate as user #1 for testing"""
    u = User.objects.get(id=1)
    u.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, u)
    return overview_redirect(request)



