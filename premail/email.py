"""Premail email templates."""
from django.conf import (
    settings,
)
from django.shortcuts import (
    render,
)

from projectify.context_processors import (
    frontend_url,
)

from .tasks import (
    send_mail,
)


class TemplateEmail:
    """Email template."""

    def __init__(self, obj):
        """Designate receiver."""
        self.obj = obj

    def get_subject_template_path(self):
        """Get path of subject template."""
        return f"{self.template_prefix}_subject.txt"

    def get_body_template_path(self):
        """Get path of body template."""
        return f"{self.template_prefix}_body.txt"

    def get_context(self):
        """Get context. To override."""
        return {
            **frontend_url(None),
            "object": self.obj,
        }

    def render_subject(self):
        """Render subject."""
        subject = render(
            None,
            self.get_subject_template_path(),
            self.get_context(),
        )
        subject = subject.content.decode()
        subject = subject.replace("\n", "")
        subject = subject.strip()
        return subject

    def render_body(self):
        """Render body."""
        return render(
            None,
            self.get_body_template_path(),
            self.get_context(),
        ).content.decode()

    def get_to_email(self):
        """Return recipient email. To override."""
        return self.obj.email

    def send(self):
        """Send email to obj."""
        if settings.EMAIL_EAGER:
            return send_mail(
                self.render_subject(),
                self.render_body(),
                self.get_to_email(),
            )
        return send_mail.delay(
            self.render_subject(),
            self.render_body(),
            self.get_to_email(),
        )
