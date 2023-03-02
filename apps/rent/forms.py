from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ObjectDoesNotExist

#Models
from apps.rent.models import *

class RegisterForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': False}), label='User Name', required=True)
    email = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': False}), label='Email', required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'style': 'text-transform: none;'}),
        label='Contraseña', required=True)
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label='Repita la contaseña', required=True)
    type = forms.ModelChoiceField(
        widget=forms.Select(),
        queryset=TypeUser.objects.all(),
        label='Tipo de Usuario',
        required=True,
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError:
            raise forms.ValidationError(' Las contraseña no es segura')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(' Las contraseñas no coinciden')
        return password2

    def clean_type(self):

        my_type = self.cleaned_data.get('type')
        try:
            objcet_type_user = TypeUser.objects.get(name=my_type)
        except Exception:
            objcet_type_user = None
        return objcet_type_user

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        object_type = self.cleaned_data['type']
        if commit:
            user.save()
            object_hitmen = GeneralUser(
                type_user = object_type,
                user = user
            )
            object_hitmen.save()
        return user


class CreateRoomsForm(forms.ModelForm):

    name_form = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'rooms'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'autocomplete': False}), label='Nombre', required=True)
    capacity = forms.IntegerField(required=True, label='Capacidad')

    class Meta:
        model = Rooms
        fields = ('name', 'capacity')


class EventsRoomsForm(forms.ModelForm):

    name_form = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'events'}))

    class Meta:
        model = EventRooms
        fields = ('name', 'date', 'rooms', 'events_type')     
        widgets = {
            'name': forms.TextInput(attrs={'required': True,}),
            'date': forms.TextInput(attrs={'class': 'datepicker', 'required': True}),
            'rooms': forms.Select(attrs={'required': True}),    
            'events_type': forms.Select(attrs={'required': True}),
        }   
        labels = {
            'name': 'Nombre*',
            'date': 'Fecha',
            'rooms': 'Salon*',
            'events_type': 'Evento*',
        }

    def __init__(self,user, *args, **kwargs):
        super(EventsRoomsForm, self).__init__(*args, **kwargs)
        self.fields['rooms'].queryset = Rooms.objects.filter(general_user__user = user)
        self.fields['events_type'].queryset = EventsType.objects.all()