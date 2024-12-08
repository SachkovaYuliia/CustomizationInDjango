# 4. Напишіть кастомний тег та фільтр для шаблонів.
# Реалізуйте власний контекстний процесор передачі глобальних даних.

from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def greeting():
    now = datetime.now()
    if now.hour < 12:
        return "Good morning!"
    elif now.hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"
