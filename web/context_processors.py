from django.conf import settings


def hostname(request):
    context = {
        'hostname': settings.HOSTNAME
    }
    return context
