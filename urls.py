# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'views.home', name='home'),
    url(r'^login/$','django.contrib.auth.views.login',{ 'template_name' : 'login.html'},name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        { 'next_page' : '/' }, name="logout"),
    url(r'^turnirs/', include('turnir.urls')),
    url(r'^admin/', include(admin.site.urls)),


    #{ 'template_name' : 'account/login.html','authentication_form' : LoginForm},

    # Examples:
    # url(r'^$', 'wargaming.views.home', name='home'),
    # url(r'^wargaming/', include('wargaming.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root' : settings.MEDIA_ROOT }),
    )
