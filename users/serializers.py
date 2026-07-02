from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    telegram_chat_id = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'telegram_chat_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        chat_id = validated_data.pop('telegram_chat_id', None)
        user = User.objects.create_user(**validated_data)
        if chat_id:
            UserProfile.objects.update_or_create(user=user, defaults={'telegram_chat_id': chat_id})
        return user
