from rest_framework import serializers
from .models import *


class TagtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagTaskMapping
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = TagtaskSerializer(
            TagTaskMapping.objects.filter(task_id=data['id']), many=True).data
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ApppuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appuser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Appuser.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
