from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255, verbose_name='Место')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=255, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Связанная привычка', related_name='main_habits'
    )
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='Периодичность (дни)')
    reward = models.CharField(max_length=255, null=True, blank=True, verbose_name='Вознаграждение')
    duration = models.PositiveSmallIntegerField(verbose_name='Время на выполнение (сек)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')
    last_reminder_date = models.DateField(null=True, blank=True, verbose_name='Дата последнего напоминания')

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError('Нельзя одновременно указать связанную привычку и вознаграждение.')
        if self.duration > 120:
            raise ValidationError('Время выполнения привычки не может превышать 120 секунд.')
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError('Связанная привычка должна быть приятной.')
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
        if not (1 <= self.periodicity <= 7):
            raise ValidationError('Периодичность должна быть от 1 до 7 дней.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"
