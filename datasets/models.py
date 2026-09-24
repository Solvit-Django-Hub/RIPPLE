import csv
import io
from django.db import models
from django.conf import settings
from projects.models import Project


class Dataset(models.Model):


    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='datasets'
    )
    name = models.CharField(max_length=150)
    file = models.FileField(upload_to='datasets/')
    rows = models.IntegerField(default=0)
    columns = models.IntegerField(default=0)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_datasets'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):

        if self.file and (self.rows == 0 or self.columns == 0):
            try:
                self.file.seek(0)
                decoded_file = self.file.read().decode('utf-8')
                reader = csv.reader(io.StringIO(decoded_file))
                header = next(reader, None)
                if header:
                    self.columns = len(header)
                    self.rows = sum(1 for _ in reader)
                self.file.seek(0)
            except Exception:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.rows} rows, {self.columns} cols) - {self.project.name}"