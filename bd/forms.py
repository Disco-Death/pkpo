from django import forms
import datetime

class UserForm(forms.Form):
    login = forms.CharField(
        widget = forms.TextInput(
        attrs={
            "class": "placeholder",
            'placeholder': 'phone',
            'pattern': "^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$",
            'autofocus': 'autofocus',
            'autocomplete': 'on',
            "id": "phone",
        }),
        min_length = 8,
        max_length = 15
        )
    password = forms.CharField(
        widget  = forms.PasswordInput(attrs={
            "class": "placeholder",
            'placeholder': 'password',
            "name": "password"
        }),
        min_length = 6
    )

class TicketForm(forms.Form):
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year, cur_year + 2)])
    date_from = forms.DateField(
        initial = datetime.date.today() + datetime.timedelta(days = 1),
        widget  = forms.SelectDateWidget(
            years = year_range,
            attrs = {
                "name": "date",
                "id": "date"
            }
        ),
        label = "Дата отправления"
    )
    from_airport = forms.ChoiceField(
        choices = (
            (1, "Уфа"),
            (2, "Москва"),
            (3, "Париж"),
            (4, "Токио"),
            (5, "Нью Йорк")
        ),
        widget = forms.Select(attrs = {
            "name": "from",
            "id": "from"
        }),
        label = "Откуда"
    )
    to_airport = forms.ChoiceField(
        choices = (
            (1, "Уфа"),
            (2, "Москва"),
            (3, "Париж"),
            (4, "Токио"),
            (5, "Нью Йорк")
        ),
        widget = forms.Select(attrs = {
            "name": "to",
            "id": "to"
        }),
        label = "Куда"
    )
    choice = forms.ChoiceField(
        choices = (
            (1, "Эконом"),
            (2, "Бизнес")
        ),
        widget = forms.Select(attrs = {
            "name": "type",
            "id": "type"
        }),
        label = "Тип"
    )
    
class CodeTicket(forms.Form):
    code = forms.CharField(
        widget = forms.TextInput(attrs={
            'placeholder': 'Код бронирования',
            'autofocus': 'autofocus',
            'autocomplete': 'on'
        }),
        label = "Код"
    )