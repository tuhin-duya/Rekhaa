"""One-time import of the repository's legacy SQLite content into Postgres."""

import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from Accounts.models import User
from Portfolio.models import ArtistModel, Category, Milestones, Painting


class Command(BaseCommand):
    help = "Import legacy SQLite data when the hosted database is empty."

    def handle(self, *args, **options):
        if User.objects.exists():
            self.stdout.write("Hosted database already contains users; legacy import skipped.")
            return

        sqlite_path = Path(settings.BASE_DIR) / "db.sqlite3"
        if not sqlite_path.exists():
            self.stdout.write("No legacy SQLite database found; import skipped.")
            return

        source = sqlite3.connect(sqlite_path)
        source.row_factory = sqlite3.Row
        with transaction.atomic():
            self._copy(source, "Accounts_user", User)
            self._copy(source, "Portfolio_artistmodel", ArtistModel)
            self._copy(source, "Portfolio_milestones", Milestones)
            self._copy(source, "Portfolio_category", Category)
            self._copy(source, "Portfolio_painting", Painting)
        source.close()
        self.stdout.write(self.style.SUCCESS("Legacy SQLite content imported."))

    def _copy(self, source, table_name, model):
        columns = {field.column for field in model._meta.concrete_fields}
        rows = source.execute(f'SELECT * FROM "{table_name}"').fetchall()
        for row in rows:
            values = {key: row[key] for key in row.keys() if key in columns}
            model.objects.update_or_create(pk=values.pop("id"), defaults=values)
        self.stdout.write(f"Imported {len(rows)} {model._meta.verbose_name_plural}.")
