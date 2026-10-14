"""WSGI configuration for Rekhaa."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rekhaa.settings")
application = get_wsgi_application()

# Vercel makes DATABASE_URL available to the function at runtime. Initialise a
# newly provisioned hosted database before serving the first request.
if os.environ.get("DATABASE_URL"):
    from django.core.management import call_command
    from django.db import connection

    if "Portfolio_artistmodel" not in connection.introspection.table_names():
        call_command("migrate", interactive=False, verbosity=0)
        call_command("import_site_data", verbosity=0)

app = application
