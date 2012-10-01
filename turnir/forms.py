# -*- coding: utf-8 -*-
from django import forms

from turnir.models import Turnir, Participant

class AddTurnir(forms.ModelForm):
    class Meta:
        model = Turnir
        fields = ['title','description','start','stop','number_prizes']

class AddParticipant(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name','last_name','rating','turnir']

class RandParticipants(forms.Form):
    n = forms.IntegerField(label=u'Количество участников турнира',required=True)
