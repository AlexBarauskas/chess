# -*- coding: utf-8 -*-
from django.db import models

class Turnir(models.Model):
    title = models.CharField(u'Наименование',max_length=128,blank=False)
    description = models.TextField(u'Описание',blank=True)
    
    start = models.DateTimeField(u'Начало турнира')
    stop = models.DateTimeField(u'Окончание турнира')

    number_rounds = models.PositiveIntegerField(u'Количество туров',null=True)

    created = models.DateTimeField(auto_now_add=True)
    
class Participant(models.Model):
    first_name = models.CharField(u'Имя',max_length=32,blank=False)
    last_name = models.CharField(u'Фамилия',max_length=32,blank=False)
    turnir =  models.ForeignKey(Turnir, null=False)
    rating = models.PositiveIntegerField(u'Рейтинг', default=0)
