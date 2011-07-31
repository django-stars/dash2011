# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


class ShoutManager(models.Manager):
    """ Custom mamger to prevent show of private shouts """
    def filter_for_user(self, user, *args, **kwargs):
        return self.get_query_set().filter(Q(is_private=False) | Q(is_private=True, user=user))

    def get_for_user(self, user, *args, **kwargs):
        return self.filter_for_user(user=user).get(*args, **kwargs)


class Shout(models.Model):
    user = models.ForeignKey(User, related_name='shouts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    message = models.TextField()
    mentions = models.ManyToManyField(User, blank=True, null=True, related_name='mentioned_in')
    # projects = models.ManyToManyField('Project', blank=True, null=True, related_name='mentioned_in')
    is_private = models.BooleanField(default=False)

    objects = ShoutManager()

    class Meta:
        ordering = ('-created',)
    
    def __unicode__(self):
        return "%s %s @ %s" % (('', '!!')[self.is_private], self.user.username, self.created)

    @models.permalink
    def get_absolute_url(self):
        return ('shout-detail', (self.id,))
