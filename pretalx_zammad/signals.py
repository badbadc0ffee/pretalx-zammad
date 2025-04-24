from django.contrib import messages
from django.dispatch import receiver
from django.template import loader
from django.urls import reverse
from pretalx.orga.signals import nav_event_settings
from pretalx.person.signals import speaker_forms
from pretalx.submission.signals import submission_forms
from requests.exceptions import ConnectionError
from zammad_py import ZammadAPI

from .forms import ZammadTicketForm
from .models import ZammadTicket


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


@receiver(submission_forms)
def pretalx_zammad_submission_forms(sender, request, submission, **kwargs):
    if submission is None:
        return []
    return pretalx_zammad_forms(
        sender, request, f"tags:{submission.code} AND close_at:>now-30d"
    )


@receiver(speaker_forms)
def pretalx_zammad_speaker_forms(sender, request, person, **kwargs):
    if person is None:
        return []
    return pretalx_zammad_forms(
        sender,
        request,
        f"(tags:{person.code} OR customer.email:{person.email}) AND close_at:>now-30d",
    )


def pretalx_zammad_forms(sender, request, query):
    forms = []
    try:
        api_url = sender.settings.zammad_url + "api/v1/"
        ticket_url = sender.settings.zammad_url + "#ticket/zoom/"
        user = sender.settings.zammad_user
        token = sender.settings.zammad_token
    except Exception:
        messages.warning(request, "Zammad plugin configuration is incomplete.")
        return forms
    try:
        client = ZammadAPI(url=api_url, username=user, http_token=token)
        tickets = client.ticket.search(query)._items
        for ticket in tickets:
            zammad_ticket = ZammadTicket(id=ticket.get("id"))
            zammad_ticket.url = ticket_url + str(ticket.get("id"))
            zammad_ticket.title = ticket.get("title")
            zammad_ticket.state = ticket.get("state")
            zammad_ticket.group = ticket.get("group")
            forms.append(ZammadTicketForm(instance=zammad_ticket))
    except ConnectionError:
        messages.warning(request, "Zammad plugin connection error.")
    except Exception:
        messages.error(request, "Zammad plugin failure")
    return forms


try:
    from samaware.signals import submission_html

    @receiver(submission_html)
    def samaware_submission_html(sender, request, submission, **kwargs):
        if submission is None:
            return None
        try:
            api_url = sender.settings.zammad_url + "api/v1/"
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
            template = loader.get_template("pretalx_zammad/samaware.html")
            context = {
                "event": sender,
                "tickets": tickets,
            }
            result = template.render(context, None)
            return result
        except ConnectionError:
            messages.warning(request, "Zammad plugin connection error.")
        except Exception:
            messages.error(request, "Zammad plugin failure")
        return None

except ImportError:
    pass
