# Generated by Django 4.0.3 on 2022-03-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rooms',
            fields=[
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('room_number', models.CharField(max_length=20)),
            ],
        ),
    ]
