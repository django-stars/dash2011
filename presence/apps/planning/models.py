from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import datetime

WORK_STATUS = (
    ('w', _('Will work from home')),
    ('a', _('Will be avaliable')),
    ('d', _('Day off'))
    )


class UserPlanManager(models.Manager):
    def user_plans(user, days):
        """ Get per user future plans for defined number of days """
        today = datetime.date.today()
        _future = today + datetime.timedelta(days=days)
        return self.filter(user=user, date__range=(today, _future))

    def today_group_status():
        """ Return list of today states for all team """
        return self.filter(date=datetime.date.today())


class DayPlan(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(_("Date"))
    work_status = models.CharField(_("Work status"),
        max_length=1, choices=WORK_STATUS)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Plan for day")
        verbose_name_plural = _("Plans")
        ordering = ("-created",)

    def __unicode__(self):
        return self.date
