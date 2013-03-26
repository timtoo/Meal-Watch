from django.contrib import admin
from models import *

import random


class MealAdmin(admin.ModelAdmin):
    list_display = ('foodtype', 'name', 'common', 'freezable', 'rating', 'last_eaten', 'created')
    list_display_links = ('name',)
    ordering = ('foodtype', 'name')
    list_filter = ['foodtype', 'common', 'freezable']
    actions_on_top = False
    actions_on_bottom = True
    list_editablen = [ 'common', 'freezable' ]

admin.site.register(Meal, MealAdmin)

class EatenAdmin(admin.ModelAdmin):
    list_display = ('date', 'meal', 'foodtype')
    ordering = ('-date', 'meal')

    def queryset(self, request):
        qs = super(EatenAdmin, self).queryset(request)
        print qs.query
        print dir(qs[0])
        print dir(qs[0].meal.foodtype)
        return qs
        #qs = qs.select_related('meal__foodtype').extra(select={'foodtype': }
        print qs.query
        print qs.values()
        return qs


    def foodtype(self, obj):
        return obj.meal.foodtype.name

admin.site.register(Eaten, EatenAdmin)

class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created')

admin.site.register(FoodType, FoodTypeAdmin)


from django.db.models import get_models, get_app
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

def autoregister(*app_list):
    for app_name in app_list:
        app_models = get_app(app_name)
        for model in get_models(app_models):
            try:
                admin.site.register(model)
            except AlreadyRegistered:
                pass

autoregister('dinner')

