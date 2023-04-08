from dotenv import load_dotenv
load_dotenv()

import os
import json
import unittest
from unittest.mock import patch
from utils.notifier import Discord

class TestDiscordNotifier(unittest.TestCase):

    def setUp(self):
        self.webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "https://example.com/webhook")
        self.discord_notifier = Discord(self.webhook_url)

    def test_init(self):
        self.assertEqual(self.discord_notifier._Discord__webhookurl, self.webhook_url, "Discord webhook URL should be set correctly")

    def test_send(self):
        msg = "Test message"
        content = {'content': msg}
        headers = {'Content-Type': 'application/json'}

        with patch("requests.post") as mock_post:
            self.discord_notifier.send(msg)
            mock_post.assert_called_once_with(self.webhook_url, json.dumps(content), headers=headers)

if __name__ == "__main__":
    unittest.main()
