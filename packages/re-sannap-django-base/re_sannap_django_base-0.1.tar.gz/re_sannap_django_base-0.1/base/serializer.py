
from rest_framework import serializers
from base.models import Province, County


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ('id', 'name')


class CreateCountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = ("id", "name", "province")


class CountySerializer(serializers.ModelSerializer):

    province_name = serializers.CharField(source='province.name')

    class Meta:
        model = County
        fields = ("id", "name", "province_name")
