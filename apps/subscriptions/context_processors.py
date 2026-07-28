from .access import has_active_subscription


def subscription_status(request):
    return {"has_active_subscription": has_active_subscription(getattr(request, "user", None))}
