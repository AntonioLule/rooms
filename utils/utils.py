from dataclasses import dataclass

#Models
from apps.rent.models import *

MODELS_GET = {
    'rooms_obj': {
        'model': Rooms,
        'query': 'general_user__user'
    },
    'events_obj': {
        'model': EventRooms,
        'query': 'rooms__general_user__user',
        'query_b': 'events_type__name'
    },
    'reserve_obj': {
        'model': Reserve,
        'query': 'general_user__user',
    },
}

@dataclass
class GetObjects:
    usr: any

    def get_type_user(self):
        try:
            type_user = GeneralUser.objects.get(user = self.usr)
        except Exception:
            type_user = None
        return type_user

    def get_objects(self,my_model_name):

        model = MODELS_GET[my_model_name]['model']
        gral_usr = self.get_type_user()
        try:
            if gral_usr.type_user.name == "Cliente" and my_model_name == 'events_obj':
                objects_rooms = model.objects.filter(**{MODELS_GET[my_model_name]['query_b']: 'Público'})
            else:
                objects_rooms = model.objects.filter(**{MODELS_GET[my_model_name]['query']: self.usr})
        except Exception:
            objects_rooms = None
        
        return objects_rooms


@dataclass
class ReserveActions:
    pk: any
    pk_customer: any

    def get_gral_usr(self):
        try:
            gral_usr = GeneralUser.objects.get(pk = self.pk_customer)
        except Exception:
            gral_usr = None
        return gral_usr

    def reservation_exist(self):
        try:
            reserve_exist = Reserve.objects.get(event_rooms__pk=self.pk, general_user__pk=self.pk_customer)
        except Exception:
            reserve_exist = None
        return reserve_exist

    def available_space_and_create(self):

        try:
            count_available = Reserve.objects.filter(event_rooms__pk=self.pk).count()
        except Exception:
            count_available = None

        try:
            event_room_object = EventRooms.objects.get(pk=self.pk)
        except Exception:
            event_room_object = None


        if count_available != None:

            if count_available<event_room_object.rooms.capacity:

                #Creo reservacion
                gral_usr = self.get_gral_usr()
                reserve_num = count_available+1
                object_reserve = Reserve(
                    reserve_num = reserve_num,
                    general_user = gral_usr,
                    event_rooms=event_room_object
                )
                object_reserve.save()
                
                return True   
            else:
                return False
        else:            
            return False

    def calcel_reserve(self):
        
        gral_usr = self.get_gral_usr()

        try:
            reserve_object = Reserve.objects.get(general_user=gral_usr, event_rooms__pk=self.pk)
            reserve_object.delete()
            return True
        except Exception as err:
            reserve_object = None
            return False            