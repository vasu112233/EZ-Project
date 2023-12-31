# Generated by Django 4.2.4 on 2023-12-19 04:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ez_backend_test', '0003_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='files',
            name='pdf',
        ),
        migrations.AddField(
            model_name='files',
            name='file',
            field=models.FileField(default='store/files/default_file.pdf', upload_to='store/files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'ppt', 'docx', 'xlsx'])]),
        ),
    ]
