from django import template
from shout.forms import ShoutForm


register = template.Library()


@register.inclusion_tag('shout/_form.html')
def shout_new_form():
	return {
		'form': ShoutForm()
	}