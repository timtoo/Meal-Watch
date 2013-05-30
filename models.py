from django.db import models
from django.contrib.auth.models import User

from managers import *

RATING_RANGE = zip(range(1,11), range(1,11))

class MealType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class FoodType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=6, blank=True, default='')
    owner = models.ForeignKey(User)

    class Meta:
        ordering = ['name']
        unique_together = ('owner', 'name',)

    def __unicode__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    foodtype = models.ForeignKey(FoodType)
    mealtype = models.ManyToManyField(MealType)
    freezable = models.BooleanField(default=False)
    prep_mins = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    common = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    last_eaten = models.DateField(null=True, editable=False, db_index=True)
    owner = models.ForeignKey(User)

    class Meta:
        ordering = ['name']
        unique_together = ('owner', 'name',)

    def __unicode__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=48, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class PeopleRating(models.Model):
    rating = models.IntegerField(choices=RATING_RANGE)
    meal = models.ForeignKey(Meal)
    person = models.ForeignKey(People)

    class Meta:
        unique_together = ('meal', 'person')

    def save(self, *args, **kwargs):
        super(PeopleRating, self).save(*args, **kwargs)
        self.meal.rating = PeopleRating.objects.filter(
                meal_id=self.meal_id).aggregate(
                models.Avg('rating'))['rating__avg']
        self.meal.save()

    def __unicode__(self):
        return u"%s / %s -> %s" % (self.person, self.meal, self.rating,)

class Eaten(models.Model):
    date = models.DateField(db_index=True)
    meal = models.ForeignKey(Meal)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = EatenManager()

    class Meta:
        verbose_name_plural = 'Eaten'

    def save(self, *args, **kwargs):
        super(Eaten, self).save(*args, **kwargs)
        self.meal.last_eaten = self.date
        self.meal.save()

    def __unicode__(self):
        return u"%s (%s)" % (self.date, self.meal)


