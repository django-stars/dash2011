import django.dispatch

state_log_changed = django.dispatch.Signal(providing_args=["old_state_log", "new_state_log"])
