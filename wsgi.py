from gather import create_app
from gather.settings import load_production_settings

application = create_app()
load_production_settings(application)

if application.config.get("SENTRY_DSN", None):
    from raven.contrib.flask import Sentry
    Sentry(application)
