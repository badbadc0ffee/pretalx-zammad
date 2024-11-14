from django.apps import AppConfig
from django.utils.translation import gettext_lazy

from . import __version__


class PluginApp(AppConfig):
    name = "pretalx_zammad"
    verbose_name = "pretalx Zammad plugin"

    class PretalxPluginMeta:
        name = gettext_lazy("pretalx Zammad plugin")
        author = "Florian Moesch"
        description = gettext_lazy("pretalx plugin for Zammad issue tracker")
        visible = True
        version = __version__
        category = "INTEGRATION"

    def ready(self):
        from . import signals  # NOQA
