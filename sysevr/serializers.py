from rest_framework import serializers
from .models import SourceCode

class SourceCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceCode
        fields = '__all__'