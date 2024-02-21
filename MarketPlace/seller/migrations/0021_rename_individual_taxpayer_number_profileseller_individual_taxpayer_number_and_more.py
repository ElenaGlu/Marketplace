# Generated by Django 4.2.7 on 2024-02-21 14:12

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0020_product_active_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profileseller',
            old_name='Individual_Taxpayer_Number',
            new_name='individual_taxpayer_number',
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profileseller',
            name='country_of_registration',
            field=django_countries.fields.CountryField(max_length=150),
        ),
        migrations.AlterField(
            model_name='tokenemailseller',
            name='token',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='tokenseller',
            name='token',
            field=models.CharField(max_length=254),
        ),
    ]
