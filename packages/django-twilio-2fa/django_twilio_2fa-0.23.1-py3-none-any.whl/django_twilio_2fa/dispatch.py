import django.dispatch


__all__ = [
    "twilio_2fa_verification_sent", "twilio_2fa_verification_success", "twilio_2fa_verification_status_changed",
    "twilio_2fa_verification_failed", "twilio_2fa_verification_retries_exceeded", "twilio_2fa_verification_start",
    "twilio_2fa_rate_limited",
]


twilio_2fa_verification_sent = django.dispatch.Signal()

twilio_2fa_verification_success = django.dispatch.Signal()

twilio_2fa_verification_status_changed = django.dispatch.Signal()

twilio_2fa_verification_failed = django.dispatch.Signal()

twilio_2fa_verification_retries_exceeded = django.dispatch.Signal()

twilio_2fa_verification_start = django.dispatch.Signal()

twilio_2fa_rate_limited = django.dispatch.Signal()
