from django import forms
from django.utils.translation import gettext_lazy as _
from hierarkey.forms import HierarkeyForm


class SettingsForm(HierarkeyForm):
    zammad_url = forms.URLField(
        label=_("Base URL"),
        widget=forms.URLInput(attrs={"placeholder": "https://zammad.org/"}),
        help_text=_("Base URL for Zammad."),
    )

    zammad_rest_api_key = forms.CharField(
        label=_("Access Token"),
        widget=forms.PasswordInput(
            attrs={"placeholder": "XXxxXxxxxxXXXXXXXxXxXxxXxxXx_xXXxXxXxXXXxXXxXXxXXXxXxxXXXXXXxxXx"},
            render_value=True,
        ),
        help_text=_("Access token for Zammad API."),
    )

    zammad_group = forms.CharField(
        label=_("Group"),
        help_text=_("Zammad group for this event."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        event = kwargs.get("obj")
        if not event.settings.zammad_group:
            self.fields["zammad_group"].initial = event.slug
