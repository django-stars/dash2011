def autodiscover():
    """
    Automatically build the activity index.
    Almost exactly as django.contrib.admin does things, for consistency.
    """
    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue
        try:
            imp.find_module('activities', app_path)
        except ImportError:
            continue

        __import__("%s.activities" % app)
