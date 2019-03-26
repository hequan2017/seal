from rest_framework import serializers
from assets.models import Ecs


class EcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ecs
        fields = '__all__'
