from django.db import models

# Models
from django.contrib.auth.models import User
from utils.models import BaseModel

class TypeUser(BaseModel):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class GeneralUser(BaseModel):

    # Llaves foraneas
    type_user = models.ForeignKey(TypeUser, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class EventsType(BaseModel):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Rooms(BaseModel):

    name = models.CharField(max_length=200)
    capacity =  models.IntegerField(default=0, null=True, blank=True)
    # Llaves foraneas
    general_user = models.ForeignKey(GeneralUser, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class EventRooms(BaseModel):
    name = models.CharField(null=True, max_length=200)
    date = models.DateField(null=True, blank=True)

    # Llaves foraneas
    rooms = models.ForeignKey(Rooms, null=True, on_delete=models.SET_NULL)
    events_type = models.ForeignKey(EventsType, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = ('date', 'rooms')


class Reserve(BaseModel):
    reserve_num = models.IntegerField(default=0, null=True, blank=True)
    # Llaves foraneas
    general_user = models.ForeignKey(GeneralUser, null=True, on_delete=models.SET_NULL)
    event_rooms = models.ForeignKey(EventRooms, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name