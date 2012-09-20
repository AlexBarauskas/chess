from django.conf.urls.defaults import patterns, include, url
urlpatterns = patterns(
    'turnir.views',
    url(r'^$', 'list_turnirs', name='list-turnirs'),
    url(r'^add/$', 'add_turnir', name='add-turnir'),
    url(r'^add/participant/$', 'add_participant', name='add-turnir'),

)
