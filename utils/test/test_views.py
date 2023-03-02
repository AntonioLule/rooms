from django.test import TestCase
from model_mommy import mommy
from faker import Faker

#Models
from django.contrib.auth.models import User
from apps.rent.models import *

#Utils
from utils.utils import GetObjects, ReserveActions

class ReservationTest(TestCase):

    def setUp(self):

        self.user = mommy.make(User)
        self.gral_usr = mommy.make('GeneralUser', user=self.user)
        self.event_type = mommy.make('EventsType', name='Público')
        self.room = mommy.make('Rooms', general_user=self.gral_usr)
        self.events_room = mommy.make('EventRooms',rooms=self.room, events_type=self.event_type)
        self.reserve = mommy.make('Reserve', general_user=self.gral_usr, event_rooms=self.events_room)
        self.instance_class = ReserveActions(pk=self.events_room.pk, pk_customer=self.gral_usr.pk)
        
    def test_reservation_exist(self):
        my_bolean = self.instance_class.reservation_exist()
        self.assertEqual(my_bolean, True)

    def test_reserve_create(self):
        my_bolean = self.instance_class.available_space_and_create()
        self.assertEqual(my_bolean, True) 

    
    def test_calcel_reserve(self):
        my_bolean = self.instance_class.calcel_reserve()
        #self.assertEqual(my_bolean, False) 
        self.assertEqual(my_bolean, True) 