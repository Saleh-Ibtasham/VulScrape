# Generated by Django 3.1.4 on 2021-04-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysevr', '0004_remove_sourcecode_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcecode',
            name='files',
            field=models.FileField(default='hello', upload_to=''),
        ),
    ]