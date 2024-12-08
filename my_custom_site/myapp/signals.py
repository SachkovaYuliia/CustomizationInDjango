from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomModel

@receiver(post_save, sender=CustomModel)
def after_save_custom_model(sender, instance, created, **kwargs):
    if created:
        print(f"New object created: {instance.title}")
    else:
        print(f"Object updated: {instance.title}")
