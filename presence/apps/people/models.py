from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save

import datetime


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))
    start_work = models.DateField(_("Start work"),
        help_text=_("Define when user start working with team."))
    vacation_days = models.PositiveIntegerField(_("Vacation days"),
        help_text=_("Vacation days for user per year."),
        default=24)
    vacation_days_used = models.PositiveIntegerField(
        _("User vacation days"),
        help_text=_("Already used vacation days this year."),
        default=0
        )
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = ("Profiles")
        ordering = ("-updated",)

    def __unicode__(self):
        return self.user.get_full_name() if \
            self.user.get_full_name() else \
            self.user.username


def create_profile(sender, **kwargs):
    """Create profile for newely created user"""
    if kwargs['created']:
        user = kwargs['instance']
        profile = Profile(user=user)
        profile.start_work = datetime.date.today()
        profile.save()

post_save.connect(create_profile, sender=User,\
    dispatch_uid="create.profile.after.user")
