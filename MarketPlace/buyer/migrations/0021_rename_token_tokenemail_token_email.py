# Generated by Django 4.2.7 on 2023-12-27 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0020_tokenemail_stop_date_tokenmain_stop_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tokenemail',
            old_name='token',
            new_name='token_email',
        ),
    ]