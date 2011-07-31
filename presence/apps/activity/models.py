import base64
try:
    import cPickle as pickle
except ImportError:
    import pickle
from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models import Q

from django_extensions.db.fields import UUIDField
from activity import utils


# TODO look for fields with build-in serialization support
# TODO add some decorator/function to auto add activity to form
# TODO add proxy model

class ActivityQuerySet(models.query.QuerySet):

    def mark_for_update(self):
        return self.update(data_for_template_cached=None)

    def for_user(self, user):
        return self.filter(Q(public=True) | Q(to_user=user))

    def by_user(self, user):
        return self.filter(user=user)

    def by_object(self, obj, activity_class, content_type=None, num=''):
        if not content_type:
            content_type = ContentType.objects.get_for_model(activity_class)
        return self.filter(**{
            'content_type': content_type,
            'obj%s_id' % str(num): obj.pk
        })

    def by_type(self, activity_type):
        content_type = ContentType.objects.get(model=activity_type)
        return self.filter(content_type=content_type)

    def send_by_email(
        self, email, template_name='activity/activity_email.txt',
        subject=_("New activity on site"), **kwargs
    ):
        '''Send activity items in queryset to given email'''

        data = kwargs
        data.update({'email': email, 'activity': self})
        body = render_to_string(template_name, data)
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])


class ActivityManager(models.Manager):
    """Contain extra difficult queries"""

    def get_query_set(self):
        return ActivityQuerySet(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)


class Activity(models.Model):
    """Store user activity in different apps. Like Facebook"""

    NONE = 0
    ADD = 1
    REMOVE = 2

    ACTION_CHOICES = (
        (NONE, _('none')),
        (ADD, _('added')),
        (REMOVE, _('removed')),
    )

    id = UUIDField(primary_key=True)
    user = models.ForeignKey(User, related_name="activity")
    time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    public = models.BooleanField(default=True)
    # if this field is set, activity feed will be shown only to this user
    to_user = models.ForeignKey(
        User, blank=True, null=True, related_name="activity_for_user"
    )
    action = models.IntegerField(blank=False, null=False)
    # Need to make effective future grouping by object
    obj_id = models.CharField(blank=True, null=True, max_length=40)
    obj2_id = models.CharField(blank=True, null=True, max_length=40)
    obj3_id = models.CharField(blank=True, null=True, max_length=40)
    obj4_id = models.CharField(blank=True, null=True, max_length=40)
    obj5_id = models.CharField(blank=True, null=True, max_length=40)
    content_type = models.ForeignKey(ContentType)
    data_for_template_cached = models.TextField(blank=True, null=True)

    objects = ActivityManager()

    def render_action(self):
        return dict(self.ACTION_CHOICES)[self.action]

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if not force_update and self.__class__.__name__ != "Activity":
            self.content_type = ContentType.objects.get_for_model(self)
        return super(Activity, self).save(
            force_insert, force_update, *args, **kwargs
        )

    def get_or_create_data_for_template(self):
        if not self.data_for_template_cached:
            current_type_model_name = self.content_type.model
            pickled = pickle.dumps(
                getattr(self, current_type_model_name).data_for_template(self),
                protocol=pickle.HIGHEST_PROTOCOL
            )
            self.data_for_template_cached = base64.encodestring(pickled)
            self.save(force_update=True)
        return pickle.loads(base64.decodestring(self.data_for_template_cached))

    def data_for_template(self, activity):
        return {'activity': self}

    def render(self, content_type=".html"):
        """Render current activity """

        current_type_model_name = self.content_type.model
        current_type_model_class = self.content_type.model_class()
        return hasattr(current_type_model_class, 'render_html') \
               and getattr(self, current_type_model_name).render_html() \
               or render_to_string(
                    "activity/%s%s" % (current_type_model_name, content_type),
                    self.get_or_create_data_for_template()
               )

    def render_email(self):
        return self.render('_email.txt').strip(' \n')

    class Meta:
        ordering = ('-time',)
        verbose_name, verbose_name_plural = "activity", "activity"

    def __unicode__(self):
        return u"Activity"

    def mark_for_update(self):
        self.data_for_template_cached = None
        self.save()


class NotifySettings(models.Model):
    """Activity notification settings for each user"""

    HOUR = 60 * 60
    HOUR6 = 60 * 60 * 6
    HOUR12 = 60 * 60 * 12
    DAY = 60 * 60 * 24
    WEEK = 60 * 60 * 24 * 7

    FREQUENCY_CHOICES = (
        (HOUR, _('every hour')),
        (HOUR6, _('4 times per day')),
        (HOUR12, _('2 time per day')),
        (DAY, _('every day')),
        (WEEK, _('every week')),
    )

    id = UUIDField(primary_key=True)
    user = models.OneToOneField(User, related_name="notify_settings")
    frequency = models.IntegerField(
        choices=FREQUENCY_CHOICES, default=DAY, verbose_name=_('frequency')
     )
    immediately = models.ManyToManyField(ContentType, blank=True, null=True)
    last_sended = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['user']

    def __unicode__(self):
        return u"%s's notify settings" % self.user

    def can_send(self, send_time=None):
        ''' check if we can send notify to user '''
        if not self.last_sended:
            return True
        if not send_time:
            send_time = datetime.now()
        return self.last_sended + timedelta(seconds=self.frequency) < send_time


@receiver(
    post_save, sender=User,
    dispatch_uid="activities.update_activity_with_updated_user_data"
)
def update_activity_with_updated_user_data(sender, instance, **kwargs):
    Activity.objects.by_user(instance).mark_for_update()


@receiver(
    post_save, sender=User,
    dispatch_uid='activities.attach_notify_settings_to_user'
)
def attach_notify_settings_to_user(sender, instance, created, **kwargs):
    if created:
        # TODO add ability to customize default immediately settings
        notify_settings = NotifySettings(user=instance)
        notify_settings.save()

utils.autodiscover()
