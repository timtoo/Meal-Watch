# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Meal.last_eaten'
        db.add_column(u'dinner_meal', 'last_eaten',
                      self.gf('django.db.models.fields.DateField')(null=True, db_index=True),
                      keep_default=False)

        # Adding index on 'Eaten', fields ['date']
        db.create_index(u'dinner_eaten', ['date'])


    def backwards(self, orm):
        # Removing index on 'Eaten', fields ['date']
        db.delete_index(u'dinner_eaten', ['date'])

        # Deleting field 'Meal.last_eaten'
        db.delete_column(u'dinner_meal', 'last_eaten')


    models = {
        u'dinner.eaten': {
            'Meta': {'ordering': "['date']", 'object_name': 'Eaten'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.Meal']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'dinner.foodtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'FoodType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dinner.meal': {
            'Meta': {'ordering': "['name']", 'object_name': 'Meal'},
            'common': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'foodtype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.FoodType']"}),
            'freezable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_eaten': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_index': 'True'}),
            'mealtype': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dinner.MealType']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'prep_mins': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'dinner.mealtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'MealType'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'dinner.people': {
            'Meta': {'ordering': "['name']", 'object_name': 'People'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '48'})
        },
        u'dinner.peoplerating': {
            'Meta': {'unique_together': "(('meal', 'person'),)", 'object_name': 'PeopleRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.Meal']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.People']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dinner']