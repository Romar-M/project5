import requests
from celery import shared_task
from django.utils import timezone
from datetime import date
from .models import Habit
from users.models import UserProfile
from django.conf import settings

@shared_task
def send_reminders():
    now = timezone.localtime().time()
    today = date.today()
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
    for habit in habits:
        if habit.last_reminder_date:
            days_passed = (today - habit.last_reminder_date).days
        else:
            days_passed = None
        if days_passed is None or days_passed >= habit.periodicity:
            profile = UserProfile.objects.filter(user=habit.user).first()
            if profile and profile.telegram_chat_id:
                message = f"Напоминание: {habit.action} в {habit.place} в {habit.time.strftime('%H:%M')}"
                send_telegram_message(profile.telegram_chat_id, message)
                habit.last_reminder_date = today
                habit.save(update_fields=['last_reminder_date'])

def send_telegram_message(chat_id, text):
    token = settings.TG_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': text})