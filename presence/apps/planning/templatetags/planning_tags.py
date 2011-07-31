from django import template
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from planning.models import DayPlan

register = template.Library()


@register.inclusion_tag("planning/tags/plans-info.html", takes_context=True)
def user_plans(context, username):
    plans = DayPlan.objects.user_plans(username)
    seven_days_plan = DayPlan.objects.user_plans(username, days=7)
    thirty_days_plan = DayPlan.objects.user_plans(username, days=30)
    data = {
        'plans': plans,
        'seven_days_plan': seven_days_plan,
        'thirty_days_plan': thirty_days_plan
    }
    return data
