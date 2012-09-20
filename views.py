# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
#from django.conf import settings
#from django.core.urlresolvers import reverse
#from django.utils import simplejson

def home(request):
    return render_to_response('base.html',
                              {},
                              RequestContext(request))
