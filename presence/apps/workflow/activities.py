import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.dispatch import receiver

from activity.models import Activity, ActivityManager
from workflow.models import State, Project, Location
from workflow.signals import state_log_changed


logger = logging.getLogger("presence.%s" % __name__)


class StateActivity(Activity):
    """Log when user change state"""

    #redefining actions
    NONE = 0
    CHANGE = 1

    ACTION_CHOICES = (
        (NONE, _('none')),
        (CHANGE, _('changed state')),
    )

    new_state = models.ForeignKey(State, related_name="new_state_activity")
    old_state = models.ForeignKey(
        State, related_name="old_state_activity", blank=True, null=True
    )
    old_state_start = models.DateTimeField(blank=True, null=True)

    objects = ActivityManager()

    def __unicode__(self):
        return 'state change from %s to %s by "%s"' % (
            self.old_state, self.new_state, self.user
        )


class ProjectActivity(Activity):
    """Log when user change project"""

    #redefining actions
    NONE = 0
    CHANGE = 1

    ACTION_CHOICES = (
        (NONE, _('none')),
        (CHANGE, _('changed project')),
    )

    new_project = models.ForeignKey(
        Project, related_name="new_project_activity"
    )
    old_project = models.ForeignKey(
        Project, related_name="old_project_activity", blank=True, null=True
    )
    old_project_start = models.DateTimeField(blank=True, null=True)

    objects = ActivityManager()

    def __unicode__(self):
        return 'project change from %s to %s by "%s"' % (
            self.old_project, self.new_project, self.user
        )


class LocationActivity(Activity):
    """Log when user change location"""

    #redefining actions
    NONE = 0
    CHANGE = 1

    ACTION_CHOICES = (
        (NONE, _('none')),
        (CHANGE, _('changed location')),
    )

    new_location = models.ForeignKey(
        Location, related_name="new_location_activity"
    )
    old_location = models.ForeignKey(
        Location, related_name="old_location_activity", blank=True, null=True
    )
    old_location_start = models.DateTimeField(blank=True, null=True)

    objects = ActivityManager()

    def __unicode__(self):
        return 'location change from %s to %s by "%s"' % (
            self.old_location, self.new_location, self.user
        )


@receiver(
    signals.post_save, sender=State,
    dispatch_uid='workflow.update_state_activity_for_changed_db'
)
def update_state(sender, instance, created, **kwargs):
    '''update activity in case when state data is changed'''

    logger.debug(
        'Updating activity with changed state "%s" data' % instance
    )
    if not created:
        StateActivity.objects.by_object(instance, StateActivity, 1) \
            .mark_for_update()
        StateActivity.objects.by_object(instance, StateActivity, 2) \
            .mark_for_update()


@receiver(
    state_log_changed,
    dispatch_uid='workflow.update_state_activity_with_changed_state'
)
def update_state_activity_with_changed_state(
    sender, old_state_log, new_state_log, **kwargs
):
    if old_state_log.state != new_state_log.state:
        logger.debug(
            'Updating activity with changed by user "%s" state' \
                % new_state_log.user
        )
        StateActivity.objects.create(
            user=old_state_log.user,
            action=StateActivity.CHANGE,
            old_state=old_state_log.state,
            obj_id=old_state_log.state.id if old_state_log.state else None,
            new_state=new_state_log.state,
            obj2_id=new_state_log.state.id,
        )


@receiver(
    state_log_changed,
    dispatch_uid='workflow.update_project_activity_with_changed_project'
)
def update_project_activity_with_changed_project(
    sender, old_state_log, new_state_log, **kwargs
):
    if old_state_log.project != new_state_log.project:
        logger.debug(
            'Updating activity with changed by user "%s" project' \
                % new_state_log.user
        )
        ProjectActivity.objects.create(
            user=old_state_log.user,
            action=ProjectActivity.CHANGE,
            old_project=old_state_log.project,
            obj_id=old_state_log.project.id if old_state_log.project else None,
            new_project=new_state_log.project,
            obj2_id=new_state_log.project.id,
        )


@receiver(
    state_log_changed,
    dispatch_uid='workflow.update_location_activity_with_changed_location'
)
def update_location_activity_with_changed_location(
    sender, old_state_log, new_state_log, **kwargs
):
    if old_state_log.location != new_state_log.location:
        logger.debug(
            'Updating activity with changed by user "%s" location' \
                % new_state_log.user
        )
        LocationActivity.objects.create(
            user=old_state_log.user,
            action=LocationActivity.CHANGE,
            old_location=old_state_log.location,
            obj_id=old_state_log.location.id \
                if old_state_log.location else None,
            new_location=new_state_log.location,
            obj2_id=new_state_log.location.id,
        )
