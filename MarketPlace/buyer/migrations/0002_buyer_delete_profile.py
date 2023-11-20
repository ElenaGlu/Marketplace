# Generated by Django 4.2.7 on 2023-11-16 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('surname', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyer.emails')),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]