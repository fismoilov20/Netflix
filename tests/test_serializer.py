from unittest import TestCase

from filmapp.models import *
from filmapp.serializers import *

class TestActorSerializer(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_actor_ser(self):
        ser = ActorSerializer(Actor.objects.get(id=1))
        print(ser.data)
        assert ser.data["country"] == "Uzbekistan"
        assert ser.data["gender"] == "Female"
        
    def test_validate_gender_valid(self):
        actor = {
            'id': 1, 
            'name': 'Feruze Normatova', 
            'country': 'Uzbekistan', 
            'gender': 'female', 
            'birth_year': '1989-09-27'
        }
        ser = ActorSerializer(data=actor)
        assert ser.is_valid() == True

    def test_validate_gender_invalid(self):
        actor = {
            'id': 1, 
            'name': 'Feruze Normatova', 
            'country': 'Uzbekistan', 
            'gender': 'femaledboy', 
            'birth_year': '1989-09-27'
        }
        ser = ActorSerializer(data=actor)
        
        assert ser.is_valid() == False

        # print(ser.errors['gender'])
        assert ser.errors['gender'][0] == "Error at gender field!"