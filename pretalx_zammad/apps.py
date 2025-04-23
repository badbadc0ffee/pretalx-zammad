from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_zammad"
    verbose_name = "pretalx Zammad plugin"

    class PretalxPluginMeta:
        name = "pretalx Zammad plugin"
        author = "Florian Moesch"
        description = gettext_lazy(
            """pretalx plugin for Zammad issue tracker.

This plugin allows you to link to tickets in a Zammad issue tracker.

The plugin will match the e-mail adresses of speakers and the six digit speaker and session codes from pretalx with the customer e-mail addresses and tags in Zammad and show the related Zammad ticket title, ticket state and ID on the speaker and session pages in the orga interface.

To manually link Zammad tickets to speakers or sessions in pretalx, you can simply add the six digit code of a speaker or a submission to the tags within Zammad.
"""
        )
        visible = True
        version = __version__
        category = "INTEGRATION"

    def ready(self):
        from . import signals  # NOQA
