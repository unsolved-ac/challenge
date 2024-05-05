from discord_webhook import DiscordWebhook
import sys

if len(sys.argv) == 1:
    print("no system arguments")
    exit()

issue_number = sys.argv[1]
issue_title = sys.argv[2]
webhook_url = sys.argv[3]


def create_content(issue_number, date, author):
    issue_url_format = "https://github.com/unsolved-ac/challenge/issues/{}"
    issue_url = issue_url_format.format(str(issue_number))

    content_format = "🍀  [{}]  challenge complete by **{}**  🍀\n\n{}"

    return content_format.format(
        date,
        author,
        issue_url
    )


def send_discord_message():
    date = issue_title.split()[1]
    author = issue_title.split()[3]

    webhook = DiscordWebhook(url=webhook_url, content=create_content(issue_number, date, author))
    webhook.execute()


def main():
    send_discord_message()


main()
