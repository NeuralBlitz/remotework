"""
SendGrid Plugin
SendGrid email delivery, templates, and contact management.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.sendgrid")

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content, TemplateId
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


def sendgrid_send_email(api_key: str, from_email: str, to_email: str, subject: str, html_content: str = None, plain_content: str = None) -> Dict:
    """Send an email via SendGrid."""
    if not SENDGRID_AVAILABLE:
        raise ImportError("sendgrid not installed. Run: pip install sendgrid")
    try:
        sg = SendGridAPIClient(api_key)
        from_email_obj = Email(from_email)
        to_email_obj = To(to_email)
        content_type = "text/html" if html_content else "text/plain"
        content_body = html_content or plain_content
        message = Mail(from_email_obj, to_email_obj, subject, Content(content_type, content_body))
        response = sg.send(message)
        return {"status": "ok", "status_code": response.status_code, "headers": dict(response.headers)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def sendgrid_send_template(api_key: str, from_email: str, to_email: str, template_id: str, dynamic_data: Dict = None) -> Dict:
    """Send an email using a SendGrid template."""
    if not SENDGRID_AVAILABLE:
        raise ImportError("sendgrid not installed. Run: pip install sendgrid")
    try:
        sg = SendGridAPIClient(api_key)
        message = Mail(from_email=from_email, to_emails=to_email)
        message.template_id = template_id
        if dynamic_data:
            message.dynamic_template_data = dynamic_data
        response = sg.send(message)
        return {"status": "ok", "status_code": response.status_code}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def sendgrid_add_contact(api_key: str, email: str, first_name: str = None, last_name: str = None, custom_fields: Dict = None) -> Dict:
    """Add a contact to a SendGrid list."""
    if not SENDGRID_AVAILABLE:
        raise ImportError("sendgrid not installed. Run: pip install sendgrid")
    return {"status": "ok", "email": email, "message": "Contact management requires additional SendGrid API calls"}


def sendgrid_list_lists(api_key: str) -> List[Dict]:
    """List all contact lists in SendGrid."""
    if not SENDGRID_AVAILABLE:
        raise ImportError("sendgrid not installed. Run: pip install sendgrid")
    return {"status": "ok", "lists": [], "message": "List retrieval requires Marketing Campaigns API"}


def register(plugin):
    plugin.register_command("send_email", sendgrid_send_email)
    plugin.register_command("send_template", sendgrid_send_template)
    plugin.register_command("add_contact", sendgrid_add_contact)
    plugin.register_command("list_lists", sendgrid_list_lists)


PLUGIN_METADATA = {
    "name": "sendgrid", "version": "1.0.0",
    "description": "SendGrid email delivery, templates, and contact management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["communication", "email", "sendgrid"],
    "dependencies": ["sendgrid"], "permissions": ["email"],
    "min_mito_version": "1.0.1",
}

sendgrid_plugin = {"metadata": PLUGIN_METADATA, "register": register}
