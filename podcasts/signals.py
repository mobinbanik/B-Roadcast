# code
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Episode
import mutagen


@receiver(pre_save, sender=Episode)
def create_episode(sender, instance: Episode, created, **kwargs):
    if created:
        print("Creating episode")
        audio_info = mutagen.File(instance.audio_file).info
        instance.duration = int(audio_info.length)
        instance.save()
