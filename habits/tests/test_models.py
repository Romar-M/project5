import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from habits.models import Habit


@pytest.mark.django_db
def test_habit_duration_validation():
    user = User.objects.create_user("testuser", password="testpass")
    with pytest.raises(ValidationError):
        h = Habit(user=user, place="дом", time="08:00:00", action="сон", duration=130)
        h.full_clean()


@pytest.mark.django_db
def test_related_habit_must_be_pleasant():
    user = User.objects.create_user("testuser2", password="testpass")
    non_pleasant = Habit.objects.create(
        user=user, place='офис', time='12:00:00', action='обед', is_pleasant=False, duration=45
    )
    with pytest.raises(ValidationError):
        h = Habit(user=user, place="парк", time="13:00:00", action="прогулка", related_habit=non_pleasant, duration=60)
        h.full_clean()
