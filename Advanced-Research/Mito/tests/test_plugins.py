"""Tests for integration plugins"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGitHubPlugin:
    def test_import(self):
        from plugins.integrations.github import GitHubClient, github_plugin
        assert github_plugin["metadata"]["name"] == "github"

    def test_client_init(self):
        from plugins.integrations.github import GitHubClient
        client = GitHubClient(token="fake")
        assert client.base_url == "https://api.github.com"
        headers = client._headers()
        assert "Authorization" in headers


class TestSlackPlugin:
    def test_import(self):
        from plugins.integrations.slack import SlackClient, slack_plugin
        assert slack_plugin["metadata"]["name"] == "slack"

    def test_client_init(self):
        from plugins.integrations.slack import SlackClient
        client = SlackClient(token="fake")
        assert "slack.com" in client.base_url


class TestDiscordPlugin:
    def test_import(self):
        from plugins.integrations.discord import DiscordClient, discord_plugin
        assert discord_plugin["metadata"]["name"] == "discord"

    def test_embed_builder(self):
        from plugins.integrations.discord import DiscordClient
        client = DiscordClient()
        embed = client.create_embed("Test", "Description", color=0xFF0000)
        assert embed["title"] == "Test"
        assert embed["color"] == 0xFF0000


class TestNotionPlugin:
    def test_import(self):
        from plugins.integrations.notion import NotionClient, notion_plugin
        assert notion_plugin["metadata"]["name"] == "notion"


class TestJiraPlugin:
    def test_import(self):
        from plugins.integrations.jira import JiraClient, jira_plugin
        assert jira_plugin["metadata"]["name"] == "jira"


class TestEmailPlugin:
    def test_import(self):
        from plugins.integrations.email_plugin import EmailClient, email_plugin
        assert email_plugin["metadata"]["name"] == "email"

    def test_client_init(self):
        from plugins.integrations.email_plugin import EmailClient
        client = EmailClient(host="smtp.test.com", port=465, use_tls=False)
        assert client.host == "smtp.test.com"
        assert client.port == 465


class TestWebhooksPlugin:
    def test_import(self):
        from plugins.integrations.webhooks import (
            WebhookHandler, WebhookSender, webhooks_plugin
        )
        assert webhooks_plugin["metadata"]["name"] == "webhooks"

    def test_handler_registration(self):
        from plugins.integrations.webhooks import WebhookHandler
        handler = WebhookHandler()
        handler.register("/test", "POST", lambda d, h: d)
        assert "/test" in handler.routes
        assert "POST" in handler.routes["/test"]

    def test_signature_verification(self):
        from plugins.integrations.webhooks import WebhookHandler
        handler = WebhookHandler(secret="mysecret")
        assert handler.verify_signature(b"test", "") is False  # no sig
        assert handler.verify_signature(b"test", "sha256=bad") is False

    def test_handler_no_secret(self):
        from plugins.integrations.webhooks import WebhookHandler
        handler = WebhookHandler()
        assert handler.verify_signature(b"test", "") is True

    def test_sender_sign(self):
        from plugins.integrations.webhooks import WebhookSender
        sender = WebhookSender(secret="mysecret")
        sig = sender.sign_payload(b"test")
        assert sig.startswith("sha256=")

    def test_sender_no_secret(self):
        from plugins.integrations.webhooks import WebhookSender
        sender = WebhookSender()
        assert sender.sign_payload(b"test") == ""


class TestRedisPlugin:
    def test_import(self):
        from plugins.integrations.redis_plugin import RedisClient, redis_plugin
        assert redis_plugin["metadata"]["name"] == "redis"


class TestS3Plugin:
    def test_import(self):
        from plugins.integrations.s3 import S3Client, s3_plugin
        assert s3_plugin["metadata"]["name"] == "s3"


class TestLLMGatewayPlugin:
    def test_import(self):
        from plugins.integrations.llm_gateway import (
            LLMGateway, OpenAIClient, AnthropicClient, llm_gateway_plugin
        )
        assert llm_gateway_plugin["metadata"]["name"] == "llm_gateway"

    def test_openai_headers(self):
        from plugins.integrations.llm_gateway import OpenAIClient
        client = OpenAIClient(api_key="fake-key")
        headers = client._headers()
        assert headers["Authorization"] == "Bearer fake-key"

    def test_anthropic_headers(self):
        from plugins.integrations.llm_gateway import AnthropicClient
        client = AnthropicClient(api_key="fake-key")
        headers = client._headers()
        assert headers["x-api-key"] == "fake-key"
        assert headers["anthropic-version"] == "2023-06-01"


class TestZapierPlugin:
    def test_import(self):
        from plugins.integrations.zapier import ZapierClient, zapier_plugin
        assert zapier_plugin["metadata"]["name"] == "zapier"


class TestTwilioPlugin:
    def test_import(self):
        from plugins.integrations.twilio import TwilioClient, twilio_plugin
        assert twilio_plugin["metadata"]["name"] == "twilio"


class TestLinearPlugin:
    def test_import(self):
        from plugins.integrations.linear import LinearClient, linear_plugin
        assert linear_plugin["metadata"]["name"] == "linear"

    def test_headers(self):
        from plugins.integrations.linear import LinearClient
        client = LinearClient(api_key="fake-key")
        headers = client._headers()
        assert headers["Authorization"] == "fake-key"


class TestCalendarPlugin:
    def test_import(self):
        from plugins.integrations.calendar import GoogleCalendarClient, calendar_plugin
        assert calendar_plugin["metadata"]["name"] == "calendar"


class TestTelegramPlugin:
    def test_import(self):
        from plugins.integrations.telegram import TelegramClient, telegram_plugin
        assert telegram_plugin["metadata"]["name"] == "telegram"

    def test_client_init(self):
        from plugins.integrations.telegram import TelegramClient
        client = TelegramClient(token="fake")
        assert "telegram.org" in client.base_url


class TestTeamsPlugin:
    def test_import(self):
        from plugins.integrations.teams import TeamsClient, teams_plugin
        assert teams_plugin["metadata"]["name"] == "teams"


class TestWhatsAppPlugin:
    def test_import(self):
        from plugins.integrations.whatsapp import WhatsAppClient, whatsapp_plugin
        assert whatsapp_plugin["metadata"]["name"] == "whatsapp"


class TestStripePlugin:
    def test_import(self):
        from plugins.integrations.stripe import StripeClient, stripe_plugin
        assert stripe_plugin["metadata"]["name"] == "stripe"

    def test_headers(self):
        from plugins.integrations.stripe import StripeClient
        client = StripeClient(api_key="sk_test_fake")
        headers = client._headers()
        assert headers["Authorization"] == "Bearer sk_test_fake"


class TestPluginsInit:
    def test_all_plugins_list(self):
        from plugins.integrations import ALL_PLUGINS
        assert len(ALL_PLUGINS) >= 270

    def test_all_plugins_have_metadata(self):
        from plugins.integrations import ALL_PLUGINS
        names = [p["metadata"]["name"] for p in ALL_PLUGINS]
        core = [
            "github", "slack", "discord", "notion", "jira", "email",
            "webhooks", "redis", "s3", "llm_gateway", "zapier",
            "twilio", "linear", "calendar", "telegram", "teams",
            "whatsapp", "stripe", "sendgrid", "salesforce", "hubspot",
            "intercom", "zendesk", "datadog", "pagerduty", "cloudflare",
            "shopify", "matrix", "supabase", "confluence", "vercel",
            "airtable", "trello", "asana", "gitlab", "sentry",
            "auth0", "okta", "clerk", "digitalocean", "heroku",
        ]
        for name in core:
            assert name in names, f"Missing core plugin: {name}"

    def test_new_plugins_exist(self):
        from plugins.integrations import ALL_PLUGINS
        names = [p["metadata"]["name"] for p in ALL_PLUGINS]
        new_plugins = [
            "pinecone", "weaviate", "mongodb", "postgresql", "elasticsearch",
            "grafana", "replicate", "huggingface", "elevenlabs",
            "firebase", "planetscale", "neon", "qdrant", "chromadb",
            "paypal", "square", "contentful", "strapi", "sanity",
            "mixpanel", "amplitude", "posthog", "segment",
            "dropbox", "google_drive", "workos", "stytch",
            "kafka", "rabbitmq", "nats", "snyk",
            "playwright", "cypress", "airbyte", "n8n",
            "cohere", "mistral", "groq", "alchemy",
            "aws_lambda", "aws_sns", "aws_sqs", "gcp_bigquery",
            "gong", "apollo", "shippo", "avalara",
            "gusto", "deel", "canvas", "strava",
            "twitter", "linkedin", "mapbox", "google_maps",
            "docusign", "quickbooks", "xero", "netsuite",
            "mlflow", "wandb", "docker_hub", "ecr",
        ]
        for name in new_plugins:
            assert name in names, f"Missing new plugin: {name}"
