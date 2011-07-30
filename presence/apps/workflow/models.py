import logging
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings


logger = logging.getLogger("presence.%s" % __name__)


class State(models.Model):

    name = models.CharField(_('name'), max_length=30)
    is_work_state = models.BooleanField(_('is work state?'), default=True, )

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_possible_next_steps(self):
        return State.objects.filter(previous_states__current_state=self)

    def get_default_next_state(self):
        return State.objects.filter(previous_states__current_state=self) \
            .order_by('-previous_states__is_default')[0]


class NextState(models.Model):

    current_state = models.ForeignKey(State, related_name="next_states")
    next_state = models.ForeignKey(State, related_name="previous_states")
    is_default = models.BooleanField(default=False)


class StateLogQuerySet(models.query.QuerySet):
    pass


class StateLogManager(models.Manager):

    def get_user_current_state_log(self, user):
        try:
            return self.order_by('-start').get(user=user, end=None)
        except StateLog.DoesNotExist:
            initial_state = State.objects.get(name=getattr(
                settings, 'INITIAL_WORKFLOW_STATE_NAME', 'Initial'
            ))
            return self.create(
                user=user, start=datetime.now(), state=initial_state
            )

    def get_query_set(self):
        return StateLogQuerySet(self.model)

    def __getattr__(self, attr, * args):
        try:
            return getattr(self.__class__, attr, * args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, * args)


class StateLog(models.Model):
    """Store information about state changes by users"""

    user = models.ForeignKey(User)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(blank=True, null=True)
    state = models.ForeignKey(State)

    objects = StateLogManager()

    class Meta:
        verbose_name = _('state log')
        verbose_name_plural = _('state logs')
        ordering = ('start',)

    def __unicode__(self):
        return "%s: %s from %s to %s" % (
            self.user, self.start, self.end, self.state
        )

    def change_state(self, next_state):
        '''
        mark current state log as ended and
        create state log for new state
        '''

        logger.info('Changing state from "%s" to "%s" for user "%s"' % (
            self.state, next_state, self.user
        ))
        now = datetime.now()
        logger.debug('Setting end value to "%s" for state log of user "%s"' % (
            str(now), self.user
        ))
        self.end = now
        self.save()
        logger.debug(
            'Creating new state log for user "%s" with start value "%s"' % (
                self.user, str(now),
            )
        )
        return StateLog.objects.create(
            user=self.user, start=now, state=next_state
        )

#class TimeLog(models.Model):
#    """Store information about tracked time in work state"""
#
#   user = models.ForeignKey(User)
#   start = models.DateTimeField(auto_now_add=True)
#   end = models.DateTimeField(blank=True, null=True)
