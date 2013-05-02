from django.conf.urls import patterns, include, url

urlpatterns = patterns('dinner.views',
    url(r'^$', 'index'),
    url(r'^(\d+)/$', 'overview'),
    url(r'^(\d+)/eaten$', 'eaten'),
    url(r'^(\d+)/meals$', 'meals'),
    url(r'^(\d+)/meals/(\d+)$', 'meals'),
    url(r'^(\d+)/meal/(\d+)$', 'meal'),
    url(r'^(\d+)/foodtypes$', 'foodtypes'),
    url(r'^(\d+)/add_eaten$', 'add_eaten'),
    url(r'^overview_redirect$', 'overview_redirect'),
    url(r'^mealtip$', 'meal_tip'),
    url(r'^auth4tim4testing$', 'auth4tim4testing'),
    url(r'^kse$', 'kse'),
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/dinner/'}),
)

