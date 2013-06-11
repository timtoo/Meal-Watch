from django.test import TestCase
from django.utils import timezone

from datetime import datetime

from dinner import views

class viewsTests(TestCase):

    def test_before_now(self):
        self.assert_(views.before_now())

        timestamp=timezone.datetime(2013, 6, 4, 1, 52, 55, 812499)

        self.assertEquals(views.before_now(timestamp=timestamp),
                datetime(2013, 6, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now(years=1, timestamp=timestamp),
                datetime(2012, 6, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('1 Year', timestamp=timestamp),
                datetime(2012, 6, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('2 years', timestamp=timestamp),
                datetime(2011, 6, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now(months=1, timestamp=timestamp),
                datetime(2013, 5, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('1 month', timestamp=timestamp),
                datetime(2013, 5, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('5 Months', timestamp=timestamp),
                datetime(2013, 1, 4, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('1 Week', timestamp=timestamp),
                datetime(2013, 5, 28, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('12 weeks', timestamp=timestamp),
                datetime(2013, 3, 12, 1, 52, 55, 812499))

        self.assertEquals(views.before_now(days=54, timestamp=timestamp),
                datetime(2013, 4, 11, 1, 52, 55, 812499))

        self.assertEquals(views.before_now('54 dayS', timestamp=timestamp),
                datetime(2013, 4, 11, 1, 52, 55, 812499))




