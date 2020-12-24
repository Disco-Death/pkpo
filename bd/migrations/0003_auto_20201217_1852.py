# Generated by Django 3.1.4 on 2020-12-17 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0002_auto_20201217_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight_Ticket',
            fields=[
                ('flight_code', models.AutoField(primary_key=True, serialize=False)),
                ('datetime_from', models.DateTimeField()),
                ('datetime_to', models.DateTimeField()),
                ('choice', models.CharField(choices=[('1', 'ECONOM'), ('2', 'BUSINESS')], default='ECONOM', max_length=1)),
                ('from_airport', models.CharField(max_length=64)),
                ('to_airport', models.CharField(max_length=64)),
                ('seat_no', models.CharField(max_length=5)),
                ('door', models.SmallIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Flight',
        ),
    ]