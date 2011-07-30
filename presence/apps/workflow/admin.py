from django.contrib import admin

from workflow.models import State, StateLog, NextState


class NextStateInline(admin.StackedInline):
    model = NextState
    fk_name = 'current_state'
    extra = 0


class StateAdmin(admin.ModelAdmin):
    inlines = [NextStateInline, ]
    list_display = ('name', 'is_work_state',)


class StateLogAdmin(admin.ModelAdmin):
    readonly_fields = ['start', 'end', 'state', 'user']
    list_display = ('user', 'state', 'start', 'end',)


admin.site.register(State, StateAdmin)
admin.site.register(StateLog, StateLogAdmin)
