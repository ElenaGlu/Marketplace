# Generated by Django 4.2.7 on 2024-02-01 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0016_tokenseller'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenseller',
            name='ProfileSeller',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='seller.profileseller'),
            preserve_default=False,
        ),
    ]