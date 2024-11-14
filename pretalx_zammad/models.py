from django.db import models




class ZammadSettings(models.Model):
    event = models.OneToOneField(
        to="event.Event",
        on_delete=models.CASCADE,
        related_name="pretalx_zammad_settings",
    )
    some_setting = models.CharField(max_length=10, default="A")
