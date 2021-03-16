"""
Package to create a telegram bot with the telepot module
"""
import collections
import telepot
import time
from typing import Union, Tuple


class Bot:
    """
    Bot telegram secured, only communicates with authorized chats

    For the moment it encapsulates a bot provided by the telepot framework.

    The management of the bot command is done through the add_command decorator
        Example:
            @bot.add_command("/start")
            def on_start(chat_id):
                bot.start_listen()
                return bot.sendMessage(chat_id, "I'm listening")

            @bot.add_command("/photo")
            def on_photo(chat_id):
                return bot.sendPhoto(chat_id, "/tmp/test.jpg", "photo")

    Commands can contain arguments
        Example for the command /hello world:
            @bot.add_command("/hello")
                def on_video(chat_id, *args):
                return bot.send_message(chat_id, "Hello " + args[0])

    :param token_id (:obj:`str`): Your bot token id
    :param chat_id (:obj:`int` | :obj:`str` | :obj:`list`): Unique identifier for the target chat
    """

    def __init__(self, token_id: str, chat_id: Union[str, int, list]):
        # Initialized a bot
        self.__bot = telepot.Bot(token_id)

        # contains the handle recorded on the customer side
        self._handle = collections.defaultdict(list)

        # Spawn a thread to received Updates
        self.__bot.message_loop(callback=self._post)

        if isinstance(chat_id, list):
            self.__chat_id = list(chat_id)
        else:
            self.__chat_id = list()
            self.__chat_id.append(int(chat_id))

        # bot status
        self._is_listen = False

    @property
    def is_listen(self) -> bool:
        """
        Get listens status.

        :return: boolean
        """
        return self._is_listen

    def start_listen(self):
        """Start listening to the bot."""
        self._is_listen = True

    def stop_listen(self):
        """Stop listening to the bot."""
        self._is_listen = False

    @staticmethod
    def run():
        """Launch the bot."""
        while True:
            time.sleep(1)

    def add_command(self, cmd: str):
        """
        Decorator to create bot commands.

        Add commands as a function in a dictionary.

        Function bot commands receive the chat_id as a parameter,

        Example:
        @bot.add_command("/start")
            def on_start(chat_id):
                bot.start_listen()
                return bot.sendMessage(chat_id, "I'm listening")


        :param cmd: command name
        """

        def __(func):
            self._handle[cmd].append(func)
            return func
        return __

    @staticmethod
    def _parse_data(data: str) -> Tuple[str, str]:
        """
        Parse data to get command and parameters.

        :param data: data received by the bot
        :return: command and parameters.
        """
        split = data.split()
        cmd = split[0]
        params = split[1:]
        return cmd, params

    def _authorized_chat_id(self, in_chat_id: int) -> bool:
        """
        Check that the incoming chat_id is authorized.

        :param in_chat_id: the incoming chat id
        :return: boolean
        """
        if in_chat_id in self.__chat_id:
            return True
        else:
            self.send_message(in_chat_id, "You're are not authorised to communicate with this Bot!")
        return False

    def _post(self, msg: dict) -> None:
        """
        Callback for :attr message_loop().

        Analyzes incoming messages. Allows to check that incoming chats are authorized
        and parse the incoming command to get the parameters

        :param msg: message received
        """
        in_chat_id = msg['chat']['id']
        data = msg['text']

        if self._authorized_chat_id(in_chat_id):
            cmd, args = self._parse_data(data)

            for handle in self._handle.get(cmd, []):
                return handle(in_chat_id, *args)

        return None

    def send_photo(self, chat_id: int, img: str, msg: str):
        """
        Uses the bot sendPhoto method.

        :param chat_id: Unique identifier for the target chat.
        :param img: image to send
        :param msg: image title
        """
        with open(img, 'rb') as photo_file:
            self.__bot.sendPhoto(chat_id, photo=photo_file, caption=msg)

    def send_message(self, chat_id: int, msg: str):
        """
        Uses the bot sendMessage method.

        :param chat_id: Unique identifier for the target chat.
        :param msg: Message to send.
        """
        self.__bot.sendMessage(chat_id, msg)

    def send_video(self, chat_id: int, video: str, msg: str):
        """
        Uses the bot sendVideo method.

        :param chat_id: Unique identifier for the target chat.
        :param video: Video file to send.
        :param msg: Video title.
        """
        with open(video, 'rb') as video_file:
            self.__bot.sendVideo(chat_id, video=video_file, caption=msg)
