from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

import datetime

DAYSTATUS = (
    ('-1', 'Bad'),
    ('0', 'Neutral'),
    ('1', 'Good')
)


class UserVoteManager(models.Manager):
    def vote(self, user, vote):
        date = datetime.date.today()
        try:
            _vote = self.get(user=user, date=date)
            _vote.vote = vote
            _vote.save()
        except:
            _vote = self.create(user=user, date=date, vote=vote)
            _vote.save()
        return _vote


class UserVote(models.Model):
    user = models.ForeignKey(User,
        verbose_name=_("User"))
    date = models.DateField(_("Current date"))
    vote = models.CharField(_("Vote"), max_length=2,
        choices=DAYSTATUS)
    objects = UserVoteManager()

    class Meta:
        verbose_name = _("User daily vote")
        verbose_name_plural = _("User daily votes")
        ordering = ("-date",)

    def __unicode__(self):
        return self.user.username
