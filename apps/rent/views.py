from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, View, TemplateView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

#Forms
from apps.rent.forms import *

#Models
from apps.rent.models import *

#Utils
from utils.utils import GetObjects, ReserveActions


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/inicio/')
    return HttpResponseRedirect('/login/')


class RegisterView(CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    form_class = RegisterForm
    template_name = 'registration/register.html'


    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['form'] =  self.form_class(self.request.GET)

        return context

    def post(self, request, *data, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            try:  # validate: unique together
                form.save()
                messages.success(request, "Registrado Correctamente")
                return HttpResponseRedirect(self.login_url)
            except Exception as er:
                messages.error(request, er.args)
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class Dashboard(LoginRequiredMixin, TemplateView):

    template_name = 'dashboard/welcome.html'



    def get_type_user(self):
        try:
            type_user = GeneralUser.objects.get(user = self.request.user)
        except Exception:
            type_user = None
        return type_user


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_objects = GetObjects(usr=self.request.user)
        context['objects_rooms'] = my_objects.get_objects('rooms_obj')
        context['objects_events'] = my_objects.get_objects('events_obj')
        context['objects_reserve'] = my_objects.get_objects('reserve_obj')
        context['grl_usr'] = my_objects.get_type_user()
        context['rooms_form'] = CreateRoomsForm()
        context['events_form'] = EventsRoomsForm(user=self.request.user)
        

        return context

    def post(self, request, **kwargs):
 
        name_form = request.POST.get('name_form')
     
        if name_form == 'rooms':
            create_rooms_form = CreateRoomsForm(request.POST)
            if create_rooms_form.is_valid():  # save address
                object_rooms = create_rooms_form.save()

                try:
                    objcet_general_user = GeneralUser.objects.get(user=self.request.user)
                except Exception:
                    objcet_general_user = None

                object_rooms.general_user = objcet_general_user
                object_rooms.save()

            else:
                messages.error(request, create_rooms_form.errors)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if name_form == 'events':
            create_events_form = EventsRoomsForm(self.request.user, request.POST)
            if create_events_form.is_valid():  # save address
                create_events_form.save()
            else:
                messages.error(request, create_events_form.errors)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/inicio/')



def delete_room(request, pk):


    try:
        events_object = EventRooms.objects.filter(rooms__pk = pk).exists()
    except Exception:
        events_object = None


    if events_object:
        messages.error(request, "No se puede eliminar aun tiene eventos")
    else:
        Rooms.objects.get(pk = pk).delete()


    return HttpResponseRedirect('/inicio/')


def create_reserve(request, pk, pk_customer):

    reservation = ReserveActions(pk=pk, pk_customer=pk_customer)
    reserve_exist = reservation.reservation_exist()

    if reserve_exist:
        messages.error(request, "Ya existe una reservacion a ese evento")
    else:
        # Verificar si hay espacio aun y si lo hay se crea la reservacion
        boolean_rst =reservation.available_space_and_create()
        if boolean_rst:
            messages.success(request, "Registrado Correctamente")
        else:
            messages.error(request, "Ya no hay espacio")
    
    return HttpResponseRedirect('/inicio/')


def cancel_reserve(request, pk, pk_customer):

    reservation = ReserveActions(pk=pk, pk_customer=pk_customer)
    reserve_canceled = reservation.calcel_reserve()

    if reserve_canceled:
        messages.success(request, "Cancelado Correctamente")
    else:
        messages.error(request, "Ha ocurrido un error al cancelar la Reservacion")

    
    return HttpResponseRedirect('/inicio/')