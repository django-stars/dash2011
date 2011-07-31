from django import template
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from planning.models import DayPlan

register = template.Library()


@register.inclusion_tag("planning/tags/plans-info.html", takes_context=True)
def user_plans(context):
    username = context['request'].user.username
    plans = DayPlan.objects.user_plans(username)
    data = {
        'plans': plans,
    }
    return data
