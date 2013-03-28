from django.conf.urls import patterns, include, url

urlpatterns = patterns('dinner.views',
    url(r'^$', 'index'),
    url(r'^(\d+)/$', 'overview'),
    url(r'^eaten$', 'eaten'),
    url(r'^meals$', 'meals'),
    url(r'^meal$', 'meal'),
    url(r'^foodtypes$', 'foodtypes'),
    url(r'^add_eaten$', 'add_eaten'),
    url(r'^overview_redirect$', 'overview_redirect'),
    url(r'^mealtip$', 'meal_tip'),
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/dinner/'}),
)

