from django.db import models


class FileStorage(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to='uploads/')
    file_name = models.CharField(max_length=255)


class DumpFileData(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey(FileStorage, models.CASCADE)
    data = models.CharField(max_length=50, blank=True, null=True)
