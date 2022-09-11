import telegram
import sys
import feedparser
import time
import datetime
import os

# Feed URL
FEED_URL = os.getenv('FEED_URL', 'https://rpilocator.com/feed/')

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError('Missing TELEGRAM_BOT_TOKEN environment variable.')

TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
if not TELEGRAM_CHAT_ID:
    raise ValueError('Missing TELEGRAM_CHAT_ID environment variable.')

# Customize the message title
MESSAGE_TITLE = 'xlocator Stock Alert'

# User Agent
USER_AGENT = 'xlocator feed alert'

# Create the message body


def formatMessage(entry):
    message = [
        f"<b><u>{MESSAGE_TITLE}</u></b>",
        f"",
        f"{entry.title}",
        f"",
        f"{entry.link}",
    ]

    message = '\n'.join(message)

    return message


bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
bot.send_message(chat_id=TELEGRAM_CHAT_ID,
                 text=f'Starting rpilocator notifier with FEED_URL={FEED_URL}...', disable_notification=True)
print(f'Starting rpilocator notifier with FEED_URL={FEED_URL}...')

# Telegram Nachricht senden


def sendMessage(message):
    try:
        result_msg = bot.sendMessage(
            chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='HTML')
        return isinstance(result_msg, telegram.message.Message)
    except Exception as err:
        print('Unhandled exception while sending telegram message: %s' %
              err, file=sys.stderr)
        return False


def updateTime(f: feedparser.FeedParserDict):
    return datetime.datetime.fromtimestamp(time.mktime(f.feed.updated_parsed))


# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL, agent=USER_AGENT)

last_find = datetime.datetime.fromtimestamp(0)
last_feed_update = updateTime(f)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entry in f.entries:
        control.append(entry.id)

# Only wait 30 seconds after initial run.
time.sleep(30)

while True:
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)
    last_feed_update = updateTime(f)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to control variable
    for entry in f.entries:
        if entry.id not in control:
            print('Found:', entry.title)
            message = formatMessage(entry)
            sendMessage(message)

            # Add entry guid to the control variable
            control.append(entry.id)
            last_find = datetime.datetime.now()

    now = datetime.datetime.now()
    print(f'Time since last find: {now - last_find}; '
          f'time since last feed update: {now - last_feed_update}.')

    time.sleep(59)
