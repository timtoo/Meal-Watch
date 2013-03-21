# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Meal.preptime'
        db.delete_column(u'dinner_meal', 'preptime')

        # Adding field 'Meal.prep_mins'
        db.add_column(u'dinner_meal', 'prep_mins',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


        # Changing field 'Meal.rating'
        db.alter_column(u'dinner_meal', 'rating', self.gf('django.db.models.fields.FloatField')(null=True))

    def backwards(self, orm):
        # Adding field 'Meal.preptime'
        db.add_column(u'dinner_meal', 'preptime',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Deleting field 'Meal.prep_mins'
        db.delete_column(u'dinner_meal', 'prep_mins')


        # Changing field 'Meal.rating'
        db.alter_column(u'dinner_meal', 'rating', self.gf('django.db.models.fields.IntegerField')(null=True))

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
            'prep_mins': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
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