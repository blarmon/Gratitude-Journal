# Generated by Django 2.1 on 2018-12-21 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0008_userextension_follows'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='user_image',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='images/'),
        ),
    ]
