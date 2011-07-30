from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as logout_


def logout(request):
    logout_(request)
    return HttpResponseRedirect("/")
