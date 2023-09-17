# Generated by Django 4.2.5 on 2023-09-17 05:35

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignemailtype',
            name='slug',
            field=autoslug.fields.AutoSlugField(allow_unicode=True, blank=True, editable=True, populate_from='name', unique=True, verbose_name='Safe URL'),
        ),
    ]
