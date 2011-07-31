from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings

import uuid
import logging

logger = logging.getLogger("presence.%s" % __name__)


class NoKeyFound(Exception):
    pass


def _generate_key():
    return uuid.uuid4().hex


class ActivationKeyManager(models.Manager):
    def create_key(self, user):
        key = self.create(user=user, key=_generate_key())
        logger.info("Generated new key %s for user %s" % \
            (user.username, key.key))
        return key

    def activate_user(self, key):
        try:
            _key = self.get(key=key)
            user = _key.user
            user.is_active = True
            user.save()
            return _key
            logger.info("Activated user %s using key %s" % \
                (user.username, _key.key))
        except self.DoesNotExist:
            logger.exeption("No user found with key %s" % key)
            raise NoKeyFound


class ActivationKey(models.Model):
    user = models.ForeignKey(User,
        verbose_name=_("User"))
    key = models.CharField(_("Key"),
        max_length=40, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ActivationKeyManager()

    class Meta:
        verbose_name = _("Activation key")
        verbose_name_plural = _("Activation keys")
        ordering = ("-created",)

    def __unicode__(self):
        return self.key
