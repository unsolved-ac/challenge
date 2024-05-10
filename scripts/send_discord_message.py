from discord_webhook import DiscordWebhook
import sys

if len(sys.argv) == 1:
    print("no system arguments")
    exit()

issue_number = sys.argv[1]
webhook_url = sys.argv[2]


def create_content(issue_number):
    issue_url_format = "https://github.com/unsolved-ac/challenge/issues/{}"
    issue_url = issue_url_format.format(str(issue_number))

    content_format = "🍀  challenge complete  🍀\n\n{}"

    return content_format.format(
        issue_url
    )


def send_discord_message():
    webhook = DiscordWebhook(url=webhook_url, content=create_content(issue_number))
    webhook.execute()


def main():
    send_discord_message()


main()
