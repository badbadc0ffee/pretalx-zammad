from django.db import models


class ZammadTicket(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
        verbose_name="Zammad numeric ticket ID",
    )
    title = models.TextField(
        verbose_name="Zammad ticket title",
    )
    state = models.TextField(
        verbose_name="Zammad ticket state",
    )
    group = models.TextField(
        verbose_name="Zammad ticket group",
    )
    url = models.URLField(
        verbose_name="Zammad ticket URL",
    )
