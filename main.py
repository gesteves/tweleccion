import logging, os

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Force Django to reload its settings.
from django.conf import settings
settings._target = None

# Must set this env var before importing any part of Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import logging
import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch.dispatcher

def log_exception(*args, **kwds):
  logging.exception('Exception in request:')

# Log errors.
django.dispatch.dispatcher.connect(
   log_exception, django.core.signals.got_request_exception)

# Unregister the rollback event handler.
django.dispatch.dispatcher.disconnect(
    django.db._rollback_on_exception,
    django.core.signals.got_request_exception)

import sys

# Uninstall Django 0.96.
for k in [k for k in sys.modules if k.startswith('django')]:
	del sys.modules[k]

# Add Django 1.0 archive to the path.
django_path = 'django.zip'
sys.path.insert(0, django_path)

# Django imports and other code go here...
import django.core.handlers.wsgi

def main():
	# Re-add Django 1.0 archive to the path, if needed.
	if django_path not in sys.path:
		sys.path.insert(0, django_path)

	# Run Django via WSGI.
	application = django.core.handlers.wsgi.WSGIHandler()
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()