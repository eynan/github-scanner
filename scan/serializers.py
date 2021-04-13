from rest_framework import serializers

from scan.models import User, Repository


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RespositorySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Repository
        exclude = ['user']
