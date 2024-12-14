from django.contrib import messages
from django.dispatch import receiver
from django.urls import reverse
from pretalx.orga.signals import nav_event_settings
from pretalx.submission.signals import submission_form_html
from requests.exceptions import ConnectionError
from zammad_py import ZammadAPI


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


@receiver(submission_form_html)
def pretalx_zammad_html_below_submission_form(sender, request, submission, **kwargs):
    if submission is None:
        return None
    try:
        api_url = sender.settings.zammad_url + "api/v1/"
        ticket_url = sender.settings.zammad_url + "#ticket/zoom/"
        user = sender.settings.zammad_user
        token = sender.settings.zammad_token
    except Exception:
        messages.warning(request, "Zammad plugin configuration is incomplete.")
        return None
    try:
        client = ZammadAPI(url=api_url, username=user, http_token=token)
        tickets = client.ticket.search(f"tags:{submission.code}")._items
        if len(tickets) == 0:
            return None
        result = ""
        result += '<div class="form-group row">'
        result += '<label class="col-md-3 col-form-label">'
        result += "Zammad"
        result += "</label>"
        result += '<div class="col-md-9">'
        for ticket in tickets:
            id = ticket["id"]
            title = ticket["title"]
            state = ticket["state"]
            group = ticket["group"]
            result += '<div class="pt-2">'
            result += '<i class="fa fa-circle-o"></i> '
            result += f"<a href='{ticket_url}{id}'>{id}</a> : {title}"
            result += (
                f'<small class="form-text text-muted">{state} in group {group}</small>'
            )
            result += "</div>"
        result += "</div>"
        result += "</div>"
        return result
    except ConnectionError:
        messages.warning(request, "Zammad plugin connection error.")
    except Exception:
        messages.error(request, "Zammad plugin failure")
    return None
