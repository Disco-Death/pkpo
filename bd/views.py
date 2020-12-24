from django.contrib.auth.models import auth, User
from django.http import *
from django.shortcuts import render
from time import gmtime, strftime
import hashlib, uuid, os, datetime
from .forms import *
from .models import *

def index(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = userform.cleaned_data.get("login")
            password = userform.cleaned_data.get("password")
            try:
                user = Client.objects.get(client_login = name)
                unknown_password = hashlib.pbkdf2_hmac(
                    'sha256',
                    password.encode('utf-8'),
                    (((user.client_story).split('\n', maxsplit = 1))[0]).encode(),
                    100000
                )
                if (user.hash_authorization == str(unknown_password)):
                    if request.user.is_authenticated:
                        auth.logout(request)
                    user = auth.authenticate(
                        username = name,
                        password = password 
                    )
                    auth.login(request, user)
                    return HttpResponseRedirect("/info")
                else:
                    return HttpResponseBadRequest("<h2>Неверный пароль!</h2>")
            except Client.DoesNotExist:
                salt = os.urandom(32)
                user, created = Client.objects.get_or_create(
                    client_login = name,
                    hash_authorization = str(
                        hashlib.pbkdf2_hmac(
                            'sha256',
                            password.encode('utf-8'),
                            (((str(salt)).split('\n', maxsplit = 1))[0]).encode(),
                            100000
                        )
                    ),
                    email = "test@gmail.com",
                    client_story = (str(salt) + "\n________________\n")
                )
                if (created):
                    user = User.objects.create_user(
                        username = name,
                        password = password
                    )
                    auth.login(request, user)
                    return HttpResponseRedirect("/info")
                else:
                    return HttpResponseServerError("Пользователь не был добавлен!")
        else:
            return HttpResponse("Как вы смогли отправить невалидные данные?!")
    else:
        userform = UserForm()
        return render(request, "index.html", {"form" : userform})

def info(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            ticketform = TicketForm(request.POST)
            if ticketform.is_valid():
                tickets = Flight_Ticket.objects.filter(
                    date_from       = ticketform.cleaned_data.get('date_from'),
                    from_airport    = int(ticketform.cleaned_data.get('from_airport')),
                    to_airport      = int(ticketform.cleaned_data.get('to_airport')),
                    choice          = ticketform.cleaned_data.get("choice"),
                    to_booked       = False
                )
                items = []
                choices = [
                    'Эконом',
                    'Бизнес'
                ]
                choices_city = [
                    "Уфа",
                    "Москва",
                    "Париж",
                    "Токио",
                    "Нью Йорк"
                ]
                for ticket in tickets:
                    items.append({
                        "from_airport"  : choices_city[int(ticket.from_airport) - 1],
                        "date_from"     : ticket.date_from,
                        "time_from"     : ticket.time_from,
                        "to_airport"    : choices_city[int(ticket.to_airport) - 1],
                        "datetime_to"   : ticket.datetime_to,
                        "choice"        : choices[int(ticket.choice) - 1],
                        "cost"          : ticket.flight_cost,
                        "seat_no"       : ticket.seat_no,
                        "door"          : ticket.door,
                        "code"          : ticket.code
                    })
                return render(
                    request,
                    "info.html",
                    {
                        "form"  : ticketform,
                        "result": True,
                        "items" : items
                    }
                )
        else:
            ticketform = TicketForm()
            return render(
                request,
                "info.html",
                {
                    "form": ticketform,
                    "result": False
                }
            )
    else:
        return HttpResponseRedirect("/index")

def info_about_ticket(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            codeticketform = CodeTicket(request.POST)
            if codeticketform.is_valid():
                code = codeticketform.cleaned_data.get("code")
                try:
                    ticket = Flight_Ticket.objects.get(code = code)
                    choices = [
                        'Эконом',
                        'Бизнес'
                    ]
                    choices_city = [
                        "Уфа",
                        "Москва",
                        "Париж",
                        "Токио",
                        "Нью Йорк"
                    ]
                    if ticket.to_booked:
                        message = " (Забронирован)"
                    else:
                        message = ""
                    return render(
                        request,
                        "info_about_ticket.html",
                        {
                            "form"          : codeticketform,
                            "code"          : code,
                            "Booked_Message": message,
                            "from_airport"  : choices_city[int(ticket.from_airport) - 1],
                            "date_from"     : ticket.date_from,
                            "time_from"     : ticket.time_from,
                            "to_airport"    : choices_city[int(ticket.to_airport) - 1],
                            "datetime_to"   : ticket.datetime_to,
                            "choice"        : choices[int(ticket.choice) - 1],
                            "cost"          : ticket.flight_cost,
                            "seat_no"       : ticket.seat_no,
                            "door"          : ticket.door
                        }
                    )
                except Flight_Ticket.DoesNotExist:
                    return render(
                        request,
                        "info_about_ticket.html",
                        {
                            "form"   : codeticketform,
                            "code"   : 0,
                            "message": "Жаль, но такие билеты не были найдены :("
                        }
                    )
        else:
            code = request.GET.get("code", "")
            codeticketform = CodeTicket()
            if not(code is None):
                try:
                    ticket = Flight_Ticket.objects.get(code = code)
                    Flight_Ticket.objects.filter(code = code).update(to_booked = True)
                    user = Client.objects.get(client_login = request.user.username)
                    new_check = Check.objects.create(
                        check_cost = ticket.flight_cost,
                        org_itn = "172856347382",
                        check_date = strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                        client_code = user
                    )
                    new_order = Order.objects.create(
                        order_date = new_check.check_date,
                        order_cost = ticket.flight_cost,
                        client_code = user
                    )
                    new_ticket = Ticket.objects.create(
                        flight = ticket.code,
                        ticket_cost = ticket.flight_cost,
                        datetime = new_order.order_date
                    )
                    order_time = Order.objects.filter(order_code = new_order.order_code)
                    new_ticket.order_code.set(order_time)
                    new_delivery = Delivery.objects.create(
                        order_code = new_order,
                        delivery_date = new_order.order_date,
                        delivery_method = 1
                    )
                    choices = [
                        'Эконом',
                        'Бизнес'
                    ]
                    choices_city = [
                        "Уфа",
                        "Москва",
                        "Париж",
                        "Токио",
                        "Нью Йорк"
                    ]
                    return render(
                        request, 
                        "info_about_ticket.html", 
                        {
                            "form"          : codeticketform,
                            "code"          : code,
                            "Booked_Message": " (Забронирован)",
                            "from_airport"  : choices_city[int(ticket.from_airport) - 1],
                            "date_from"     : ticket.date_from,
                            "time_from"     : ticket.time_from,
                            "to_airport"    : choices_city[int(ticket.to_airport) - 1],
                            "datetime_to"   : ticket.datetime_to,
                            "choice"        : choices[int(ticket.choice) - 1],
                            "cost"          : ticket.flight_cost,
                            "seat_no"       : ticket.seat_no,
                            "door"          : ticket.door,
                            "code"          : ticket.code
                        }
                    )
                except Flight_Ticket.DoesNotExist:
                    return render(
                        request, 
                        "info_about_ticket.html",
                        {
                            "form": codeticketform,
                            "code": 0,
                            "message": "Введите ваш номер бронирования в форму выше"
                        }
                    )
            else:
                return HttpResponseBadRequest("<h2>Сторонний запрос отклонён!</h2>")
    else:
        return HttpResponseRedirect("/index")

def easter_egg(request):
    return render(request, "easter_egg.html")