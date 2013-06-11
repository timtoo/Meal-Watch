from django.conf.urls import patterns, include, url

urlpatterns = patterns('dinner.views',
    url(r'^$', 'index'),
    url(r'^(\d+)/$', 'overview'),
    url(r'^(\d+)/overview_table$', 'overview_table'),
    url(r'^(\d+)/eaten$', 'eaten'),
    url(r'^(\d+)/eaten/new$', 'eaten_edit'),
    url(r'^(\d+)/eaten/(\d+)/edit$', 'eaten_edit'),
    url(r'^(\d+)/meals$', 'meals'),
    url(r'^(\d+)/meals/(\d+)$', 'meals'),
    url(r'^(\d+)/meal/new$', 'meal_edit'),
    url(r'^(\d+)/meal/(\d+)/edit$', 'meal_edit'),
    url(r'^(\d+)/meal/(\d+)$', 'meal'),
    url(r'^(\d+)/foodtypes$', 'foodtypes'),
    url(r'^(\d+)/foodtype/new$', 'foodtype_edit'),
    url(r'^(\d+)/foodtype/(\d+)/edit$', 'foodtype_edit'),
    url(r'^overview_redirect$', 'overview_redirect'),
    url(r'^(\d+)/mealtip$', 'meal_tip'),
    url(r'^auth4tim4testing$', 'auth4tim4testing'),
    url(r'^kse$', 'kse'),
)

urlpatterns += patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/dinner/'}),
)

