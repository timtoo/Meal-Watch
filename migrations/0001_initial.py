# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MealType'
        db.create_table(u'dinner_mealtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'dinner', ['MealType'])

        # Adding model 'FoodType'
        db.create_table(u'dinner_foodtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'dinner', ['FoodType'])

        # Adding model 'Meal'
        db.create_table(u'dinner_meal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('foodtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dinner.FoodType'])),
            ('freezable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('preptime', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('common', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'dinner', ['Meal'])

        # Adding M2M table for field mealtype on 'Meal'
        db.create_table(u'dinner_meal_mealtype', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('meal', models.ForeignKey(orm[u'dinner.meal'], null=False)),
            ('mealtype', models.ForeignKey(orm[u'dinner.mealtype'], null=False))
        ))
        db.create_unique(u'dinner_meal_mealtype', ['meal_id', 'mealtype_id'])

        # Adding model 'People'
        db.create_table(u'dinner_people', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=48)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'dinner', ['People'])

        # Adding model 'PeopleRating'
        db.create_table(u'dinner_peoplerating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'dinner', ['PeopleRating'])

        # Adding M2M table for field meal on 'PeopleRating'
        db.create_table(u'dinner_peoplerating_meal', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('peoplerating', models.ForeignKey(orm[u'dinner.peoplerating'], null=False)),
            ('meal', models.ForeignKey(orm[u'dinner.meal'], null=False))
        ))
        db.create_unique(u'dinner_peoplerating_meal', ['peoplerating_id', 'meal_id'])

        # Adding model 'Eaten'
        db.create_table(u'dinner_eaten', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('meal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dinner.Meal'])),
        ))
        db.send_create_signal(u'dinner', ['Eaten'])


    def backwards(self, orm):
        # Deleting model 'MealType'
        db.delete_table(u'dinner_mealtype')

        # Deleting model 'FoodType'
        db.delete_table(u'dinner_foodtype')

        # Deleting model 'Meal'
        db.delete_table(u'dinner_meal')

        # Removing M2M table for field mealtype on 'Meal'
        db.delete_table('dinner_meal_mealtype')

        # Deleting model 'People'
        db.delete_table(u'dinner_people')

        # Deleting model 'PeopleRating'
        db.delete_table(u'dinner_peoplerating')

        # Removing M2M table for field meal on 'PeopleRating'
        db.delete_table('dinner_peoplerating_meal')

        # Deleting model 'Eaten'
        db.delete_table(u'dinner_eaten')


    models = {
        u'dinner.eaten': {
            'Meta': {'object_name': 'Eaten'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.Meal']"}),
            'notes': ('django.db.models.fields.TextField', [], {})
        },
        u'dinner.foodtype': {
            'Meta': {'object_name': 'FoodType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'dinner.meal': {
            'Meta': {'object_name': 'Meal'},
            'common': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'foodtype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.FoodType']"}),
            'freezable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mealtype': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dinner.MealType']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'preptime': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dinner.mealtype': {
            'Meta': {'object_name': 'MealType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'dinner.people': {
            'Meta': {'object_name': 'People'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '48'})
        },
        u'dinner.peoplerating': {
            'Meta': {'object_name': 'PeopleRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dinner.Meal']", 'symmetrical': 'False'}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dinner']