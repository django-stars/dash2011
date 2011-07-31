import logging
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User

from activity.models import Activity, ActivityManager
from shout.models import Shout


logger = logging.getLogger("presence.%s" % __name__)


class ShoutActivity(Activity):
    """Log when user shout something"""

    #redefining actions
    NONE = 0
    SHOUT = 1

    ACTION_CHOICES = (
        (NONE, _('none')),
        (SHOUT, _('shouted')),
    )

    shout = models.ForeignKey(Shout)

    objects = ActivityManager()

    def __unicode__(self):
        return 'user "%s" shouted "%s"' % (
            self.user, self.shout
        )


@receiver(
    signals.post_save, sender=Shout,
    dispatch_uid='shout.update_shout_activity_for_news_shout'
)
def update_shourt_activity_with_new_shout(sender, instance, created, **kwargs):
    if created:
        logger.debug(
            'Updating activity with new shout by user "%s" vote' % instance.user
        )
        if not instance.is_private:
            logger.debug(
                'Creating public shout activity for shout by user "%s"' % instance.user
            )
            ShoutActivity.objects.create(
                user=instance.user,
                action=ShoutActivity.SHOUT,
                shout=instance
            )
        else:
            logger.debug(
                'Shout is not public, creating activity for author "%s"' % instance.user
            )
            ShoutActivity.objects.create(
                user=instance.user,
                action=ShoutActivity.SHOUT,
                shout=instance,
                public=False,
                to_user=instance.user
            )
            for user in instance.mentions.all():
                logger.debug(
                    'creating shout activity for mentioned user "%s"' % user
                )
                ShoutActivity.objects.create(
                    user=instance.user,
                    action=ShoutActivity.SHOUT,
                    shout=instance,
                    public=False,
                    to_user=user
                )
