# -*- coding: utf-8 -*-
from django import forms

from turnir.models import Turnir, Participant

class AddTurnir(forms.ModelForm):
    class Meta:
        model = Turnir
        fields = ['title','description','start','stop']

class AddParticipant(forms.ModelForm):
    class Meta:
        model = Participant
