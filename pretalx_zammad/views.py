from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from pretalx.common.views.mixins import PermissionRequired


from .forms import ZammadSettingsForm


class ZammadSettingsView(PermissionRequired, FormView):
    permission_required = "orga.change_settings"
    template_name = "pretalx_zammad/settings.html"
    form_class = ZammadSettingsForm

    def get_success_url(self):
        return self.request.path

    def get_object(self):
        return self.request.event

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["event"] = self.request.event
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("The pretalx Zammad plugin settings were updated."))
        return super().form_valid(form)
