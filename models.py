from django.db import models

RATING_RANGE = zip(range(1,11), range(1,11))

class MealType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class FoodType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=48, unique=True)
    created = models.DateTimeField(auto_now_add=True)

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
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    meal = models.ForeignKey(Meal)

    class Meta:
        ordering = [ 'date' ]
        verbose_name_plural = 'Eaten'

    def save(self, *args, **kwargs):
        super(Eaten, self).save(*args, **kwargs)
        self.meal.last_eaten = self.date
        self.meal.save()

    def __unicode__(self):
        return u"%s (%s)" % (self.date, self.meal)


