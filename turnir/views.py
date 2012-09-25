# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from turnir.models import Turnir,Participant,Game
from turnir.forms import AddTurnir, AddParticipant, RandParticipants

from account.decorators import referee_required

from random import randint

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
    if turnir.raund_set.count() and turnir.raund_set.count()<turnir.cur_raund_id:
        final = turnir.participant_set.all().order_by('position')[:turnir.number_prizes]
    else:
        final=[]
    return render_to_response('turnir-view.html',
                              {'turnir':turnir,
                               'tab':request.session.get('tab','participants'),
                               'final':final},
                              RequestContext(request))
@referee_required
def rand_parts(request,turnir_id):
    turnir = get_object_or_404(Turnir,id=turnir_id)
    if request.method == "POST":
        form = RandParticipants(request.POST)
        if form.is_valid():
            n = form.cleaned_data['n']
            #print 'N=%s'%n
            for i in xrange(n):
                Participant(first_name='Участник',last_name=str(i),
                            rating=randint(1,2000),turnir=turnir).save()
            return HttpResponseRedirect(reverse('view-turnir',args=[turnir_id]))
    else:
        form = RandParticipants()
    return render_to_response('form.html',
                              {'btn_title':u'Сгенерировать участников',
                               'form':form},
                              RequestContext(request))

@referee_required
def generate_table(request,turnir_id):
    turnir = get_object_or_404(Turnir,id=turnir_id)
    turnir.create_table_raunds()
    request.session['tab']='table'
    return HttpResponseRedirect(reverse('view-turnir',args=[turnir_id]))

@referee_required
def add_participant(request,turnir_id):
    turnir = get_object_or_404(Turnir,id=turnir_id)
    request.session['tab']='participants'
    return base_add(request,AddParticipant,
                    reverse('view-turnir',args=[turnir_id]),
                    {'turnir':turnir})

@referee_required
def generate_next_raund(request,turnir_id):
    if request.method=='POST':
        for key in request.POST:
            #print request.POST
            if key.startswith('game'):
                w = request.POST[key]
                g = get_object_or_404(Game,id=key.split('-')[1])
                if not w:
                    g.participant1.points+=0.5
                    g.participant2.points+=0.5
                    g.participant1.save()
                    g.participant2.save()
                else:
                    p=get_object_or_404(Participant,id=w)
                    g.winner = p
                    g.save()
                    p.points+=1
                    p.save()
        get_object_or_404(Turnir,id=turnir_id).calc_next_round()
    request.session['tab']='table'
    return HttpResponseRedirect(reverse('view-turnir',args=[turnir_id]))
    
