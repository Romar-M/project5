from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'last_reminder_date')

    def validate(self, data):
        if data.get('related_habit') and data['related_habit'].user != self.context['request'].user:
            raise serializers.ValidationError("Связанная привычка должна принадлежать вам.")
        return data