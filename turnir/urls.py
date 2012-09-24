from django.conf.urls.defaults import patterns, include, url
urlpatterns = patterns(
    'turnir.views',
    url(r'^$', 'list_turnirs', name='list-turnirs'),
    url(r'^add/$', 'add_turnir', name='add-turnir'),
    url(r'^(?P<turnir_id>\d+)/participant/add/$', 'add_participant', name='add-participant'),
    url(r'^(?P<turnir_id>\d+)/$', 'view_turnir', name='view-turnir'),

    url(r'^(?P<turnir_id>\d+)/create-table$', 'generate_table', name='generate-table'),
    url(r'^(?P<turnir_id>\d+)/save-raund$', 'generate_next_raund',name='save-raund'),
)
