# Generated by Django 2.1 on 2018-12-09 23:09

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0006_journal_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]