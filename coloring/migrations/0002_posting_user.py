# Generated by Django 3.2.13 on 2022-04-14 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=70)),
                ('qty', models.IntegerField()),
                ('qty_units', models.CharField(choices=[('UN', 'Units'), ('LB', 'Pounds'), ('OZ', 'Ounces'), ('PT', 'Pints'), ('GL', 'Gallons')], default='UN', max_length=2)),
                ('best_by', models.DateField()),
                ('private', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=300)),
                ('active', models.BooleanField(default=True)),
                ('unopened', models.BooleanField(default=False)),
                ('og_packaging', models.BooleanField(default=False)),
                ('store_bought', models.BooleanField(default=False)),
                ('homemade', models.BooleanField(default=False)),
                ('listing_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coloring.user')),
            ],
        ),
    ]
