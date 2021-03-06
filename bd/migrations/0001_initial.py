# Generated by Django 3.1.4 on 2020-12-17 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('client_code', models.AutoField(primary_key=True, serialize=False)),
                ('client_login', models.CharField(max_length=15)),
                ('hash_authorization', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('client_story', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_code', models.AutoField(primary_key=True, serialize=False)),
                ('datetime_from', models.DateTimeField()),
                ('datetime_to', models.DateTimeField()),
                ('from_airport', models.CharField(max_length=64)),
                ('to_airport', models.CharField(max_length=64)),
                ('seat_no', models.CharField(max_length=4)),
                ('door', models.SmallIntegerField()),
                ('choice', models.CharField(choices=[('1', 'ECONOM'), ('2', 'BUSINESS')], default='ECONOM', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_code', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField()),
                ('order_cost', models.FloatField()),
                ('client_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bd.client')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_code', models.AutoField(primary_key=True, serialize=False)),
                ('flight', models.TextField()),
                ('ticket_cost', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('order_code', models.ManyToManyField(to='bd.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateTimeField()),
                ('delivery_method', models.CharField(choices=[('1', 'EMAIL'), ('2', 'PICKUP')], default='EMAIL', max_length=1)),
                ('order_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bd.order')),
            ],
        ),
        migrations.CreateModel(
            name='Check',
            fields=[
                ('check_code', models.AutoField(primary_key=True, serialize=False)),
                ('check_cost', models.FloatField()),
                ('org_itn', models.CharField(max_length=12)),
                ('check_date', models.DateTimeField()),
                ('add_info', models.TextField()),
                ('client_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bd.client')),
            ],
        ),
    ]
