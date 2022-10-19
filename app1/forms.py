from django import forms
from django.contrib.auth.forms import UserCreationForm

from app1.models import Login, Bill, Equipments


class TrainerForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('username','password1','password2','name','age','email','address','contact_no','photo')


class Product(forms.ModelForm):
    class Meta:
        model = Equipments
        fields = '__all__'


class AddBill(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Login.objects.filter(is_customer=True))

    class Meta:
        model = Bill
        exclude = ('status',)


class CustomerForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('username','password1','password2','name','age','email','address','contact_no','photo')