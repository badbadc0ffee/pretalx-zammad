import random

from django.dispatch import receiver
from django.urls import reverse
from pretalx.orga.signals import nav_event_settings
from pretalx.submission.signals import submission_details


@receiver(nav_event_settings)
def pretalx_zammad_settings(sender, request, **kwargs):
    if not request.user.has_perm("orga.change_settings", request.event):
        return []
    return [
        {
            "label": "Zammad",
            "url": reverse(
                "plugins:pretalx_zammad:settings",
                kwargs={"event": request.event.slug},
            ),
            "active": request.resolver_match.url_name
            == "plugins:pretalx_zammad:settings",
        }
    ]


@receiver(submission_details)
def pretalx_zammad_submission_details(sender, request, submission, **kwargs):
    result = ""
    result += '<div class="form-group row">'
    result += '<label class="col-md-3 col-form-label">'
    result += "Zammad"
    result += "</label>"
    result += '<div class="col-md-9">'
    result += '<div class="pt-2">'
    result += '<i class="fa fa-circle-o" style="color: #f9a557"></i> '
    result += f'<a href="#">{random.randrange(20000, 29999)}</a> : '
    result += "Illegal Instructions"
    result += "</div>"
    result += '<div class="pt-2">'
    result += '<i class="fa fa-circle-o" style="color: #3aa57c"></i> '
    result += f'<a href="#">{random.randrange(20000, 29999)}</a> : '
    result += "Inverse transitional encoding"
    result += "</div>"
    result += '<div class="pt-2">'
    result += '<i class="fa fa-circle-o" style="color: #3aa57c"></i> '
    result += f'<a href="#">{random.randrange(20000, 29999)}</a> : '
    result += "Versatile foreground monitoring"
    result += "</div>"
    result += "</div>"
    result += "</div>"
    return result
