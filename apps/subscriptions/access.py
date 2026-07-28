def has_active_subscription(user) -> bool:
    if not user or not user.is_authenticated:
        return False
    subscription = getattr(user, "subscription", None)
    if subscription is None:
        return False
    return subscription.is_active
