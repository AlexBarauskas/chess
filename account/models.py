# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(u'Роль',
                            max_length=1,
                            choices=(('s','Судья'),
                                     ('p','Участник'),
                                     ('o','другое'),
                                     ),
                            default='s')    
    
    class Meta:
        verbose_name = u'Аккаунт'
        verbose_name_plural = u'Аккаунты'

    def __unicode__(self):
        return unicode(self.user)
