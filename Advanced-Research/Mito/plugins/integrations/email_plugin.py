"""
Email Plugin (SMTP)
Send emails via SMTP with attachments and HTML support
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Any

logger = logging.getLogger("mito.plugins.email")


class EmailClient:
    def __init__(self, host: Optional[str] = None, port: Optional[int] = None,
                 username: Optional[str] = None, password: Optional[str] = None,
                 use_tls: bool = True):
        self.host = host or os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.port = port or int(os.environ.get("SMTP_PORT", "587"))
        self.username = username or os.environ.get("SMTP_USERNAME", "")
        self.password = password or os.environ.get("SMTP_PASSWORD", "")
        self.use_tls = use_tls

    def send(self, to: List[str], subject: str, body: str, html: str = None,
             cc: List[str] = None, bcc: List[str] = None,
             attachments: List[str] = None, from_addr: str = None) -> Dict:
        msg = MIMEMultipart("alternative")
        msg["From"] = from_addr or self.username
        msg["To"] = ", ".join(to)
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = ", ".join(cc)

        msg.attach(MIMEText(body, "plain"))
        if html:
            msg.attach(MIMEText(html, "html"))

        if attachments:
            for filepath in attachments:
                self._attach_file(msg, filepath)

        all_recipients = to + (cc or []) + (bcc or [])

        try:
            with smtplib.SMTP(self.host, self.port, timeout=30) as server:
                if self.use_tls:
                    server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.sendmail(msg["From"], all_recipients, msg.as_string())

            logger.info(f"Email sent to {to}: {subject}")
            return {"success": True, "to": to, "subject": subject}
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {"success": False, "error": str(e)}

    def _attach_file(self, msg: MIMEMultipart, filepath: str):
        with open(filepath, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(filepath)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)

    def send_template(self, to: List[str], subject: str, template: str,
                      variables: Dict[str, str] = None, **kwargs) -> Dict:
        body = template
        html = None
        if variables:
            for key, value in variables.items():
                body = body.replace(f"{{{{{key}}}}}", value)
        return self.send(to, subject, body, **kwargs)


def email_send_cmd(to: str = "", subject: str = "", body: str = "") -> Dict:
    """Send an email via SMTP."""
    client = EmailClient()
    recipients = [addr.strip() for addr in to.split(",")]
    return client.send(recipients, subject, body)


def email_send_html_cmd(to: str = "", subject: str = "", html: str = "") -> Dict:
    """Send an HTML email via SMTP."""
    client = EmailClient()
    recipients = [addr.strip() for addr in to.split(",")]
    return client.send(recipients, subject, body="", html=html)


def register(plugin):
    plugin.register_command("email_send", email_send_cmd)
    plugin.register_command("email_send_html", email_send_html_cmd)
    plugin.set_resource("client_class", EmailClient)


PLUGIN_METADATA = {
    "name": "email",
    "version": "1.0.0",
    "description": "Email integration - SMTP with HTML and attachments",
    "author": "Mito Team",
    "license": "MIT",
    "tags": ["email", "smtp", "notifications"],
    "dependencies": [],
    "permissions": ["network_access", "read_env"],
    "min_mito_version": "1.0.0",
}


email_plugin = {
    "metadata": PLUGIN_METADATA,
    "register": register,
}
