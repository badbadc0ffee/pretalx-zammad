from django import forms
from django.utils.translation import gettext_lazy as _
from hierarkey.forms import HierarkeyForm
from pretalx.common.forms.renderers import TabularFormRenderer

from .models import ZammadTicket


class SettingsForm(HierarkeyForm):
    zammad_url = forms.URLField(
        label=_("Base URL"),
        widget=forms.URLInput(attrs={"placeholder": "https://zammad.org/"}),
        help_text=_("Base URL for Zammad"),
    )

    zammad_user = forms.CharField(
        label=_("User"),
        help_text=_("Username for Zammad API"),
    )

    zammad_token = forms.CharField(
        label=_("Access Token"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "XXxxXxxxxxXXXXXXXxXxXxxXxxXx_xXXxXxXxXXXxXXxXXxXXXxXxxXXXXXXxxXx"
            },
        ),
        help_text=_("Access token for Zammad API"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ZammadRenderer(TabularFormRenderer):
    form_template_name = "pretalx_zammad/form.html"


class ZammadTicketForm(forms.ModelForm):
    default_renderer = ZammadRenderer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].disabled = True

    class Meta:
        model = ZammadTicket
        exclude = ["id"]
