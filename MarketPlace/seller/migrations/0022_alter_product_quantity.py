# Generated by Django 4.2.7 on 2024-02-21 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0021_rename_individual_taxpayer_number_profileseller_individual_taxpayer_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]