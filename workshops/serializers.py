from rest_framework import serializers
from workshops.models import Hobby, Location, Workshop


class WorkshopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workshop
        fields = '__all__'