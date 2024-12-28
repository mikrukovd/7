import ptbot
import os

from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def timeout(chat_id, bot):
    text = 'Время вышло'
    bot.send_message(chat_id, text)


def notify_progress(secs_left, chat_id, bot, message_id, time):
    text = 'Осталось {} секунд\n{}'.format(secs_left, render_progressbar(time, time-secs_left))
    bot.update_message(chat_id, message_id, text)


def reply(author_id, author_message, bot):
    time = parse(author_message)
    text = 'Осталось {} секунд\n{}'.format(time, render_progressbar(time, 0))
    message_id = bot.send_message(author_id, text)
    bot.create_countdown(time, notify_progress, chat_id=author_id, bot=bot, message_id=message_id, time=time)
    bot.create_timer(time, timeout, chat_id=author_id, bot=bot)


def main():
    load_dotenv()
    tg_token = os.getenv('TOKEN_TELEGA')
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
