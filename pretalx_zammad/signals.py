from django.contrib import messages
from django.dispatch import receiver
from django.template import loader
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
def pretalx_zammad_submission_form_html(sender, request, submission, **kwargs):
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
        template = loader.get_template("pretalx_zammad/zammad_submission_form.html")
        context = {
            "tickets": tickets,
            "ticket_url": ticket_url,
        }
        result = template.render(context, None)
        return result
    except ConnectionError:
        messages.warning(request, "Zammad plugin connection error.")
    except Exception:
        messages.error(request, "Zammad plugin failure")
    return None


try:
    from samaware.signals import submission_html

    @receiver(submission_html)
    def samaware_submission_html(sender, request, submission, **kwargs):
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
            template = loader.get_template("pretalx_zammad/zammad_submission.html")
            context = {
                "tickets": tickets,
                "ticket_url": ticket_url,
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
