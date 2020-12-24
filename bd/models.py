from django.db import models

class Client(models.Model):
    client_code         = models.AutoField(primary_key = True)
    client_login        = models.CharField(max_length = 15)
    hash_authorization  = models.TextField()
    email               = models.EmailField()
    client_story        = models.TextField()

class Check(models.Model):
    check_code  = models.AutoField(primary_key = True)
    check_cost  = models.FloatField()
    org_itn     = models.CharField(max_length = 12)
    check_date  = models.DateTimeField()
    client_code = models.ForeignKey(
        Client,
        on_delete = models.CASCADE,
    )
    add_info    = models.TextField()

class Order(models.Model):
    order_code  = models.AutoField(primary_key = True)
    order_date  = models.DateTimeField()
    order_cost  = models.FloatField()
    client_code = models.ForeignKey(
        Client,
        on_delete = models.CASCADE,
    )

class Ticket(models.Model):
    ticket_code = models.AutoField(primary_key = True)
    flight      = models.TextField()
    ticket_cost = models.FloatField()
    datetime    = models.DateTimeField()
    order_code  = models.ManyToManyField(Order)

class Delivery(models.Model):
    order_code      = models.OneToOneField(
        Order,
        on_delete = models.CASCADE,
    )
    delivery_date   = models.DateTimeField()
    methods = (
        ('1', 'EMAIL'),
        ('2', 'PICKUP'),
    )
    delivery_method = models.CharField(
        max_length  = 1,
        choices     = methods,
        default     = 'EMAIL',
    )
    
class Flight_Ticket(models.Model):
    flight_code     = models.AutoField(primary_key = True)
    code            = models.TextField(unique = True)
    date_from       = models.DateField()
    time_from       = models.TimeField()
    datetime_to     = models.DateTimeField()
    choices = (
        ('1', 'ECONOM'),
        ('2', 'BUSINESS'),
    )
    choice          = models.CharField(
        max_length = 1,
        choices = choices,
        default = 'ECONOM'
    )
    from_airport    = models.CharField(max_length = 64)
    to_airport      = models.CharField(max_length = 64)
    seat_no         = models.CharField(max_length = 5)
    door            = models.SmallIntegerField()
    flight_cost     = models.FloatField()
    to_booked       = models.BooleanField(default = False)