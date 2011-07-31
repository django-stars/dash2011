from django.db import models


class EventPublishedManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return super(EventPublishedManager, self).get_query_set(*args, **kwargs).filter(is_published=True)


class Event(models.Model):
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    is_published = models.BooleanField(default=True)
    no_time = models.BooleanField(default=False)
    message = models.TextField()

    objects = models.Manager()
    published = EventPublishedManager()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return u"%s @ %s" % (self.title, self.date)

    @models.permalink
    def get_absolute_url(self):
        return ('event-detail', (self.id,))
