# Generated by Django 2.1 on 2018-12-11 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0007_auto_20181209_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='follows',
            field=models.ManyToManyField(related_name='followed_by', to='journals.UserExtension'),
        ),
    ]
