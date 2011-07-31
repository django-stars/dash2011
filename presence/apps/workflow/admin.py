from django.contrib import admin

from workflow.models import State, StateLog, NextState, Project, Location
from workflow.activities import StateActivity


class NextStateInline(admin.StackedInline):
    model = NextState
    fk_name = 'current_state'
    extra = 0


class StateAdmin(admin.ModelAdmin):
    inlines = [NextStateInline, ]
    list_display = ('name', 'is_work_state',)


class StateLogAdmin(admin.ModelAdmin):
    readonly_fields = ['start', 'end', 'state', 'user']
    list_display = ('user', 'state', 'project', 'location', 'start', 'end',)


admin.site.register(State, StateAdmin)
admin.site.register(StateLog, StateLogAdmin)
admin.site.register(Project)
admin.site.register(Location)
