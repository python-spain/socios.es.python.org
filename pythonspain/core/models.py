import io
import logging

from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from pythonspain.core.files import UploadToDir

logger = logging.getLogger(__name__)


class BaseImport(TimeStampedModel):
    """Abstract model to implement an asynchronous import process."""

    IDLE, RUNNING, FINISHED, ERROR = 0, 1, 2, 3
    STATUSES = (
        (IDLE, _("Idle")),
        (RUNNING, _("Running")),
        (FINISHED, _("Finished")),
        (ERROR, _("Error")),
    )

    data = models.FileField(
        _("data"), upload_to=UploadToDir("imports", random_name=False)
    )

    status = models.SmallIntegerField(
        _("status"), choices=STATUSES, default=IDLE, blank=True
    )
    items = models.PositiveIntegerField(_("items"), null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Import #{self.pk}"

    def source(self):
        """Creates the source for the importer using the data file."""
        file_content = self.data.read()
        source = io.BytesIO()
        source.write(file_content)
        source.seek(0)
        return source

    def importer(self):
        """Gets the import helper function that does the import."""
        raise NotImplementedError()

    def importer_task(self):
        """Gets the async task that does the import."""
        raise NotImplementedError()

    def import_data(self, async_process=False):
        """Executes the import process."""
        if self.status != self.IDLE:
            return  # Only import if is idle
        if async_process:
            task = self.importer_task()
            task.delay(self.pk)
        else:
            self.items = 0
            self.status = self.RUNNING
            self.save()
            # Import line by line to don't load all the file in memory
            self.data.seek(0)
            importer = self.importer()
            try:
                items = importer(source=self.source())
                self.items = items.count()
                self.status = self.FINISHED
                self.save()
            except Exception as exception:
                self.status = self.ERROR
                self.save()
                raise exception


class BaseExport(TimeStampedModel):
    """Abstract model to implement an asynchronous export process."""

    IDLE, RUNNING, FINISHED, ERROR = 0, 1, 2, 3
    STATUSES = (
        (IDLE, _("Idle")),
        (RUNNING, _("Running")),
        (FINISHED, _("Finished")),
        (ERROR, _("Error")),
    )

    data = models.FileField(
        upload_to=UploadToDir("exports", random_name=False),
        null=True,
        blank=True,
        verbose_name=_("data"),
    )

    status = models.SmallIntegerField(
        _("status"), choices=STATUSES, default=IDLE, blank=True
    )
    items = models.PositiveIntegerField(_("items"), null=True, blank=True)

    FILE_NAME = "export"
    FILE_EXTENSION = "csv"

    class Meta:
        abstract = True

    def __str__(self):
        return "Export #%s" % self.pk

    def get_queryset(self):
        """Gets the QuerySet to export."""
        raise NotImplementedError()

    def exporter(self):
        """Gets the export helper function that does the export."""
        raise NotImplementedError()

    def exporter_task(self):
        """Gets the async task that does the exporter."""
        raise NotImplementedError()

    def export_data(self, async_process=False):
        """Executes the import process."""
        if self.status != self.IDLE:
            return  # Only import if is idle
        if async_process:
            task = self.exporter_task()
            task.delay(self.pk)
        else:
            self.items = 0
            self.status = self.RUNNING
            self.save()
            # Export data and save it in the file field
            exporter = self.exporter()
            output = io.StringIO()
            try:
                items = exporter(self.get_queryset(), output)
                output.seek(0)
                content = output.getvalue()
                self.data.save(
                    f"{self.FILE_NAME}-{self.created.strftime('%Y%m%d')}.{self.FILE_EXTENSION}",
                    content=ContentFile(content.encode("utf-8")),
                )
                self.items = items
                self.status = self.FINISHED
                self.save()
            except Exception as exception:
                self.status = self.ERROR
                self.save()
                raise exception
