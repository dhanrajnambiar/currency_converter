from django import forms
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.models import User

class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']


class convertForm(forms.Form):
    options = [
        ('Select','Select'),('USD','USD'),('INR','INR'),('EUR','EUR'),('SGD','SGD'),('GBP','GBP')
    ]

    field1 = forms.ChoiceField(
        choices = options,
        initial = '0',
        required = True,
        label = "FROM"
    )

    field2 = forms.ChoiceField(
        choices = options,
        initial = '0',
        required = True,
        label = "TO"
    )

    field3 = forms.DecimalField(required = True, min_value = 0)

class loginForm(forms.Form):
    username = forms.CharField(max_length = 200)
    password = forms.CharField(widget = forms.PasswordInput)

    def clean_username(self):
        inst_username = self.cleaned_data.get("username")
        return inst_username

    def clean_password(self):
        inst_password = self.cleaned_data.get("password")
        return inst_password
