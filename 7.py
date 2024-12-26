import ptbot
import os

from pytimeparse import parse
from dotenv import load_dotenv


TG_TOKEN = os.getenv('TOKEN_TELEGA')
BOT = ptbot.Bot(TG_TOKEN)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def answer(chat_id):
    BOT.send_message(chat_id, 'Время вышло')


def notify_progress(secs_left, chat_id, message_id, time):
    text = ('Осталось {} секунд\n{}').format(secs_left, render_progressbar(time, time-secs_left))
    BOT.update_message(chat_id, message_id, text)


def reply(chat_id, message):
    time = parse(message)
    text = ('Осталось {} секунд\n{}').format(time, render_progressbar(time, 0))
    message_id = BOT.send_message(chat_id, text)
    BOT.create_countdown(time, notify_progress, message_id=message_id, chat_id=chat_id, time=time)
    BOT.create_timer(time, answer, chat_id=chat_id)


def main():
    BOT.reply_on_message(reply)
    BOT.run_bot()


if __name__ == '__main__':
    load_dotenv()
    main()
