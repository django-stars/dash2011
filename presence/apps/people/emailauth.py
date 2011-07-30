#-*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import email_re


class EmailBackend(ModelBackend):
    """ Authenticate via e-mail address """
    def authenticate(self, username=None, password=None):
        # If username is an email address, then try it
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        # We have a non-email address username we should try username
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
