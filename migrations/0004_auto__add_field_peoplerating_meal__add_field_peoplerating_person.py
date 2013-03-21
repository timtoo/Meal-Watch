# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PeopleRating.meal'
        db.add_column(u'dinner_peoplerating', 'meal',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['dinner.Meal']),
                      keep_default=False)

        # Adding field 'PeopleRating.person'
        db.add_column(u'dinner_peoplerating', 'person',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['dinner.People']),
                      keep_default=False)

        # Removing M2M table for field meal on 'PeopleRating'
        db.delete_table('dinner_peoplerating_meal')


    def backwards(self, orm):
        # Deleting field 'PeopleRating.meal'
        db.delete_column(u'dinner_peoplerating', 'meal_id')

        # Deleting field 'PeopleRating.person'
        db.delete_column(u'dinner_peoplerating', 'person_id')

        # Adding M2M table for field meal on 'PeopleRating'
        db.create_table(u'dinner_peoplerating_meal', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('peoplerating', models.ForeignKey(orm[u'dinner.peoplerating'], null=False)),
            ('meal', models.ForeignKey(orm[u'dinner.meal'], null=False))
        ))
        db.create_unique(u'dinner_peoplerating_meal', ['peoplerating_id', 'meal_id'])


    models = {
        u'dinner.eaten': {
            'Meta': {'ordering': "['date']", 'object_name': 'Eaten'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
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
            'Meta': {'object_name': 'PeopleRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.Meal']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dinner.People']"}),
            'rating': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['dinner']
