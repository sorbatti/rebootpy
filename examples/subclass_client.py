"""This example showcases how to use rebootpy within a subclass. If captcha
is enforced for the accounts, you will only have to enter the authorization code
the first time you run this script.

NOTE: This example uses AdvancedAuth and stores the details in a file.
It is important that this file is moved whenever the script itself is moved
because it relies on the stored details. However, if the file is nowhere to
be found, it will simply use device code to generate a new file.
"""

import rebootpy
import json
import os

from rebootpy.ext import commands


filename = 'device_auths.json'
description = 'My awesome fortnite bot!'


def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}


def store_device_auth_details(details):
    with open(filename, 'w') as fp:
        json.dump(details, fp)


class MyBot(commands.Bot):
    def __init__(self):
        device_auth_details = get_device_auth_details()
        super().__init__(
            command_prefix='!',
            description=description,
            auth=rebootpy.AdvancedAuth(
                prompt_device_code=True,
                open_link_in_browser=True,
                **device_auth_details
            )
        )

    async def event_device_auth_generate(self, details):
        store_device_auth_details(details)

    async def event_ready(self):
        print(f'Bot ready as {self.user.display_name} ({self.user.id}).')

    async def event_friend_request(self, request):
        await request.accept()

    async def event_friend_message(self, message):
        print('Received message from {0.author.display_name} | Content: "{0.content}"'.format(message))
        await message.reply('Thanks for your message!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello there!')


bot = MyBot()
bot.run()
