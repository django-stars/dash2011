import logging
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver

from activity.models import Activity, ActivityManager
from vote.models import UserVote, DAYSTATUS


logger = logging.getLogger("presence.%s" % __name__)


class VoteActivity(Activity):
    """Log when user change or add vote"""

    #redefining actions
    NONE = 0
    CHANGE = 1

    ACTION_CHOICES = (
        (NONE, _('none')),
        (CHANGE, _('voted')),
    )

    vote = models.CharField(_("Vote"), max_length=2, choices=DAYSTATUS)

    objects = ActivityManager()

    def __unicode__(self):
        return 'vote change to %s by "%s"' % (
            self.vote, self.user
        )


@receiver(
    signals.post_save, sender=UserVote,
    dispatch_uid='vote.update_vote_activity_for_changed_vote'
)
def update_vote_activity_with_changed_vote(sender, instance, created, **kwargs):
    logger.debug(
        'Updating activity with changed by user "%s" vote' % instance.user
    )
    VoteActivity.objects.create(
        user=instance.user,
        action=VoteActivity.CHANGE,
        vote=instance.vote
    )
