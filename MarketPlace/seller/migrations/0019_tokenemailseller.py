# Generated by Django 4.2.7 on 2024-02-02 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0018_rename_profileseller_tokenseller_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenEmailSeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField()),
                ('stop_date', models.DateTimeField(default=None)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.profileseller')),
            ],
        ),
    ]
