from rest_framework import serializers
from .models import Dictionary, DictionaryElement


class RefbookSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Dictionary
        fields = ['id', 'code', 'name']


class RefbookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictionaryElement
        fields = ['code', 'value']
