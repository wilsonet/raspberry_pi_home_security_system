#!/usr/bin/env python
"""Home security system."""
import time


from lib.camera import Camera
from lib.bot import Bot
from lib.pir import MotionDetector
from config import TOKEN_ID, REGISTRATION_FOLDER, VIDEO_TIME, CHAT_ID

camera = Camera(REGISTRATION_FOLDER)
bot = Bot(TOKEN_ID, CHAT_ID)
pir = MotionDetector()


@bot.add_command("/start")
def on_start(chat_id):
    """
    Add command /start: Start bot listening.

    :param chat_id: Unique identifier for the target chat provide by the bot.
    """
    bot.start_listen()
    return bot.send_message(chat_id, "Start motion detection.")


@bot.add_command("/stop")
def on_stop(chat_id):
    """
    Add command /stop: Stop bot listening.

    :param chat_id: Unique identifier for the target chat provide by the bot.
    """
    bot.stop_listen()
    return bot.send_message(chat_id, "Stop motion detection.")


@bot.add_command("/status")
def on_status(chat_id):
    """
    Add command /status: show listening status.

    :param chat_id: Unique identifier for the target chat provide by the bot.
    """
    msg = "Motion detection is running." if bot.is_listen else "Motion detection is off."
    return bot.send_message(chat_id, msg)


@bot.add_command("/photo")
def on_photo(chat_id):
    """
    Add command /photo: take a photo.

    :param chat_id: Unique identifier for the target chat provide by the bot.
    """
    return bot.send_photo(chat_id, camera.take_photo(), "capture")


@bot.add_command("/video")
def on_video(chat_id, v_time):
    """
    Add command /video: record a video.

    :param chat_id: Unique identifier for the target chat provide by the bot.
    :param v_time: duration for the recording of the video.
    """
    delay = v_time if v_time else VIDEO_TIME
    bot.send_message(chat_id, "Recording video start")
    return bot.send_video(chat_id, camera.start_recording(delay), "video")


@bot.add_command("/help")
def on_help(chat_id):
    """
    Add command /help: show help.

    :param chat_id: Unique identifier for the target chat provide by the bot.
    """
    msg = "command usage:\n"
    msg += "\t/start : start the home monitoring system \n"
    msg += "\t/stop  : stop the home monitoring system\n"
    msg += "\t/status  : show the status of the monitoring system \n"
    msg += "\t/photo : take a picture\n"
    msg += "\t/video <delay> : records a video, by default delay is " + str(VIDEO_TIME) + "s \n"
    msg += "\t/clean : remove all files in video folder\n"
    msg += "\t/help  : show help\n"
    return bot.send_message(chat_id, msg)


@bot.add_command("/clean")
def on_clean(chat_id):
    """
    Add command /clean: remove file in REGISTRATION_FOLDER

    :param chat_id: Unique identifier for the target chat provide by the bot.
    """
    return bot.send_message(chat_id, camera.purge_records())


print('I am listening ...')
try:
    while True:
        if bot.is_listen and pir.movement_detected():
            bot.send_video(CHAT_ID, camera.start_recording(VIDEO_TIME), 'motion detected')
        else:
            time.sleep(1)
except KeyboardInterrupt:
    del camera
