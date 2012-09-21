# -*- coding: utf-8 -*-
from django.db import models
import math

class Turnir(models.Model):
    title = models.CharField(u'Наименование',max_length=128,blank=False)
    description = models.TextField(u'Описание',blank=True)
    
    start = models.DateTimeField(u'Начало турнира')
    stop = models.DateTimeField(u'Окончание турнира')

    number_rounds = models.PositiveIntegerField(u'Количество туров',null=True)
    number_prizes = models.PositiveIntegerField(u'Количество призовых мест', default=3)
    registration = models.BooleanField(u'Допустима ли регистрация участников',default=True)

    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = u'Турнир'
        verbose_name_plural = u'Турниры'

    def __unicode__(self):
        return self.title

    def create_table_raunds(self):
        parts = Participant.objects.filter(turnir=self).order_by('-rating')
        N = parts.count()
        if N<2:
            return u'В турнире зарегистрировано менее двух участников!'
        k = self.number_prizes
        M = sum( map(lambda x:[math.ceil(x)-1,math.ceil(x)][math.ceil(x)-x<=0.5],[math.log(N,2),math.log(k,2)]))
        self.number_rounds=M
        r=Raund(turnir = self, number = 1)
        r.save()
        if M>1:
            for i in xrange(2,M+1):
                Raund(turnir = self, number = i).save()
        if N%2 == 1:
            p = parts[N-1]
            parts=parts[:N]
            Game(turnir=self,raund=r,
                 participant1=p,winner=p).save()
        for i in xrange(N/2):
            Game(turnir=self,raund=r,
                 participant1=parts[i],participant2=parts[N/2+i]).save()
        self.register = False
        self.save()

    
class Participant(models.Model):
    first_name = models.CharField(u'Имя',max_length=32,blank=False)
    last_name = models.CharField(u'Фамилия',max_length=32,blank=False)
    turnir =  models.ForeignKey(Turnir, null=False)
    rating = models.PositiveIntegerField(u'Рейтинг', default=0)

    class Meta:
        verbose_name = u'Участник'
        verbose_name_plural = u'Участники'

    def __unicode__(self):
        return '%s %s'%(self.first_name,self.last_name)

class Raund(models.Model):
    turnir = models.ForeignKey(Turnir, null=False)
    number = models.PositiveIntegerField(u'Номер тура', default=0)

    def __unicode__(self):
        return u'Тур №%s'%self.number

class Game(models.Model):
    start = models.DateTimeField(u'Начало игры',null=True)
    stop = models.DateTimeField(u'Окончание игры',null=True)
    turnir = models.ForeignKey(Turnir, null=False)
    raund = models.ForeignKey(Raund, null=False)
    participant1 = models.ForeignKey(Participant, null=False,
                                     related_name='games1')
    participant2 = models.ForeignKey(Participant, null=True,
                                     related_name='games2')
    winner = models.ForeignKey(Participant, null=True,
                                     related_name='wins')


    
