# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from turnir.models import Turnir
from turnir.forms import AddTurnir, AddParticipant


def list_turnirs(request):
    return render_to_response('index.html',
                              {'turnirs':Turnir.objects.all()},
                              RequestContext(request))

def base_add(request,FORM):
    if request.method == 'POST':
        form = FORM(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list-turnirs'))
    else:
        form = FORM()
    return render_to_response('form.html',
                              {'btn_title':u'Сохранить',
                               'form':form,
                               },
                              RequestContext(request))
@login_required
def add_turnir(request):
    return base_add(request,AddTurnir)

@login_required
def add_participant(request):
    return base_add(request,AddParticipant)


