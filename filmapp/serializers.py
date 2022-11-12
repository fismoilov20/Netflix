from .models import *

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

class ActorSerializer(ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

    def validate_gender(self, value):
        if value.lower() != 'male' and value.lower() != 'female':
            raise ValidationError("Error at gender field!")
        return value

class MovieSerializer(ModelSerializer):
    actors = ActorSerializer(many=True)            ## 'actors' — column name in Movie model
    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        return self.create(validated_data)

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'