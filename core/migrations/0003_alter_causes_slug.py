# Generated by Django 4.0.3 on 2022-04-30 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_causes_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='causes',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
