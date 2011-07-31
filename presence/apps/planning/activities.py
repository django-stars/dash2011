import logging
from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver

from activity.models import Activity, ActivityManager
from planning.models import DayPlan, WORK_STATUS


logger = logging.getLogger("presence.%s" % __name__)


class PlanningActivity(Activity):
    """Log when user change or add planning"""

    #redefining actions
    NONE = 0
    ADDED = 1

    ACTION_CHOICES = (
        (NONE, _('none')),
        (ADDED, _('added')),
    )

    plan = models.ForeignKey(DayPlan)

    objects = ActivityManager()


@receiver(
    signals.post_save, sender=DayPlan,
    dispatch_uid='planning.update_planning_activity_for_changed_planning'
)
def update_planning_activity_with_changed_planning(sender, instance, created, **kwargs):
    logger.debug(
        'Updating activity with changed by user "%s" planning' % instance.user
    )
    PlanningActivity.objects.create(
        user=instance.user,
        action=PlanningActivity.ADDED,
        plan=instance
    )
