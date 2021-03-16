#!/usr/bin/env python
"""
Testing bot package.
"""
import unittest
import sys
import os
import site

site.addsitedir('..')
from lib.bot import Bot
from config import TOKEN_ID, REGISTRATION_FOLDER, CHAT_ID

if TOKEN_ID == 'Your_token_id' or not os.path.exists(REGISTRATION_FOLDER):
    print("Variables bot_id or registration_folder are not defined in config.py")
    sys.exit(1)


class TestBotMethods(unittest.TestCase):
    """Test Bot class."""

    @classmethod
    def setUpClass(cls):
        cls.bot = Bot(TOKEN_ID, CHAT_ID)
        cls.chat_id = int(CHAT_ID)

    def authorised(self):
        """Checks if the bot accepts other chats_id than the authorized."""
        self.assertEqual(self.bot._authorized_chat_id(18545452), False, "The method self.bot._authorized_chat_id "        
                                                                        "doesn't work")

    def test_bot_status(self):
        """Test method bot.is_listen."""
        self.assertEqual(self.bot.is_listen, 0, "Bot is listen")

    def test_set_start_listen(self):
        """Test setter bot.start_listen."""
        self.bot.start_listen()
        self.assertEqual(self.bot.is_listen, True, "Cannot set Bot.is_listen to ON")

    def test_set_stop_listen(self):
        """Test setter bot.stop_listen."""
        self.bot.stop_listen()
        self.assertEqual(self.bot.is_listen, 0, "Cannot set Bot.is_listen to OFF")

    def test_add_command(self):
        """Test decorator add_command"""

        @self.bot.add_command("/testsuite")
        def on_test(chat_id):
            return chat_id

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459,
               'text': '/testsuite',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._post(msg), self.chat_id, "Decorator add_command doesn't function")

    def test_send_message(self):
        """Test send message."""

        @self.bot.add_command("/message")
        def on_test(chat_id):
            return self.bot.send_message(chat_id, "Test send message")

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459,
               'text': '/message',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._post(msg), None, "Send message doesn't function")

    def test_send_photo(self):
        """Test send photo."""

        @self.bot.add_command("/photo")
        def on_test_photo(chat_id):
            return self.bot.send_photo(chat_id, 'testsuite/logo-ok.png', "Testsuite")

        msg = {'message_id': 305,
               'chat': {'id': self.chat_id,
                        'first_name': 'test',
                        'last_name': 'test',
                        'type': 'private'},
               'date': 1586725459, 'text': '/photo',
               'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}
        self.assertEqual(self.bot._post(msg), None, "Send photo doesn't function")


if __name__ == '__main__':
    unittest.main()
