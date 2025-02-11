from django.db import models
from rest_framework import serializers

from app.models import *
from app.serializers import *

class AdminUserSerializer(serializers.Serializer):
    id                  = serializers.ReadOnlyField()
    first_name           = serializers.CharField(max_length=100)
    last_name           = serializers.CharField(max_length=100)
    email               = serializers.EmailField(max_length=200)
    permissions         = serializers.CharField(max_length=1, help_text="\'S' for staff, \'A' for admin", required=False)
    staff               = serializers.BooleanField(default=False)
    admin               = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name      = validated_data.get("first_name", instance.first_name)
        instance.last_name      = validated_data.get("last_name", instance.last_name)
        instance.email          = validated_data.get("email", instance.email)
        instance.permissions    = validated_data.get("permission", instance.permissions)
        instance.staff          = validated_data.get("staff", instance.staff)
        instance.admin          = validated_data.get("admin", instance.admin)
        
        instance.save()
        return instance

class InternAdminSerializer(serializers.ModelSerializer):
    stack = StackSerializer(many=True)
    class Meta:
        model = Intern
        fields = [
            "id",
            "username",
            "full_name",
            "stack",
            "state",
            "gender",
            "about",
            "batch",
            "current_salary",
            "employed",
            "picture",
        ]

    def create(self, validated_data):
        stacks_data = validated_data.pop('stack')
        intern = Intern.objects.create(**validated_data)
        for stack_data in stacks_data:
            Stack.objects.create(intern=intern, **stack_data)
        return intern