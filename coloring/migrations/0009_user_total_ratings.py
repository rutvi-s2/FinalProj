# Generated by Django 3.2.13 on 2022-04-27 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0008_auto_20220425_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_ratings',
            field=models.IntegerField(null=True),
        ),
    ]
