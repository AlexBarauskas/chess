# -*- coding: utf-8 -*-
from django.db import models
from django.template.loader import render_to_string
import math

class Turnir(models.Model):
    title = models.CharField(u'Наименование',max_length=128,blank=False)
    description = models.TextField(u'Описание',blank=True)
    start = models.DateTimeField(u'Начало турнира')
    stop = models.DateTimeField(u'Окончание турнира')
    number_prizes = models.PositiveIntegerField(u'Количество призовых мест', default=3)

    number_rounds = models.PositiveIntegerField(u'Количество туров',null=True)
    registration = models.BooleanField(u'Допустима ли регистрация участников',default=True)
    cur_raund_id =  models.PositiveIntegerField(u'Номер текущего раунда', null=True)
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
        Game.objects.filter(turnir=self, raund__number=1).delete()
        Raund.objects.filter(turnir = self).delete()
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
        self.cur_raund_id = r.number
        self.save()

    def calc_next_round(self):
        if self.cur_raund_id<self.number_rounds:
            self.cur_raund_id += 1
            r=Raund.objects.get(turnir = self, number = self.cur_raund_id)
            #r.save()
            groups = []; gr=None
            parts = Participant.objects.filter(turnir=self).order_by('-points','-rating')
            while parts:
                p = parts[0]
                if gr:
                    last_p = gr[len(gr)-1].id
                else:
                    last_p = None
                gr = Participant.objects.filter(turnir=self, points=p.points).order_by('-points','-rating')
                if last_p:
                    gr = gr.exclude(id=last_p)
                    
                parts = Participant.objects.filter(turnir=self).filter(points__lt=p.points).order_by('-points','-rating')
                if gr.count()%2 and parts.count():
                    gr = list(gr)+[parts[0]]
                    parts = parts[1:]
                groups.append(gr)
            for gr in groups:
                N = len(gr)
                for i in xrange(N/2):
                    
                    Game(turnir=self,raund=r,
                         participant1=gr[i],participant2=gr[N/2+i]).save()
                if N%2:
                    Game(turnir=self,raund=r,
                         participant1=gr[N-1],winner=gr[N-1]).save()
            
        elif self.cur_raund_id == self.number_rounds:
            self.cur_raund_id += 1
            parts = self.participant_set.all().order_by('-points')
            i=1
            for p in parts:
                p.position=i
                p.save()
                i+=1
        self.save()
        

    def render_table(self):
        #parts = Participant.objects.filter(turnir=self).order_by('-rating')
        N = self.participant_set.count()
        table = [["<td> </td><td> </td>" for i in range(self.number_rounds)] for j in range(N/2+N%2)]
        i = 1
        games = Game.objects.filter(turnir=self, raund__number=i)
        while games:
            j = 0
            for g in games:
                table[j][i-1]=render_to_string('table-call.html',
                                               {'P1':g.participant1,
                                                'P2':g.participant2 or '',
                                                'W':g.winner,
                                                'game':g})
                j+=1
            i+=1
            games = Game.objects.filter(turnir=self, raund__number=i)
        tag = map(lambda x:'<tr>'+'\n'.join(x)+'</tr>',table)
        return '\n'.join(tag)
    
class Participant(models.Model):
    first_name = models.CharField(u'Имя',max_length=32,blank=False)
    last_name = models.CharField(u'Фамилия',max_length=32,blank=False)
    turnir =  models.ForeignKey(Turnir, null=False)
    rating = models.PositiveIntegerField(u'Рейтинг', default=0)
    points = models.FloatField(u'Очки набранные в турнире', default=0)
    position =  models.PositiveIntegerField(u'Место в турнире', default=0)

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


    
