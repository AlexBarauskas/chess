# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from turnir.models import Turnir
from turnir.forms import AddTurnir, AddParticipant

from account.decorators import referee_required

def list_turnirs(request):
    return render_to_response('index.html',
                              {'turnirs':Turnir.objects.all()},
                              RequestContext(request))

def base_add(request,FORM,success_url,initial={}):
    if request.method == 'POST':
        form = FORM(request.POST,initial=initial)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(success_url)
    else:
        form = FORM(initial=initial)
    return render_to_response('form.html',
                              {'btn_title':u'Сохранить',
                               'form':form,
                               },
                              RequestContext(request))
@referee_required
def add_turnir(request):
    return base_add(request,AddTurnir,reverse('list-turnirs'))

def view_turnir(request,turnir_id):
    turnir = get_object_or_404(Turnir,id=turnir_id)
    return render_to_response('turnir-view.html',
                              {'turnir':turnir},
                              RequestContext(request))

def generate_table(request,turnir_id):
    turnir = get_object_or_404(Turnir,id=turnir_id)
    turnir.create_table_raunds()
    return HttpResponseRedirect(reverse('view-turnir',args=[turnir_id]))

@referee_required
def add_participant(request,turnir_id):
    turnir = get_object_or_404(Turnir,id=turnir_id)
    return base_add(request,AddParticipant,
                    reverse('view-turnir',args=[turnir_id]),
                    {'turnir':turnir})


