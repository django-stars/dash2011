from django.contrib import admin

from models import UserVote


class UserVoteAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'vote', 'date')

admin.site.register(UserVote, UserVoteAdmin)
