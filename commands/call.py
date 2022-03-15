from datetime import datetime, timedelta, tzinfo, timezone
from random import choice
from tokenize import group
import json

import pytz

import asyncio

import aiofiles


from dis_snek import (
    ContextMenu,
    OptionTypes,
    SlashCommandChoice,
    context_menu,
    slash_command,
    slash_option,
    InteractionContext,
    Embed,
    CommandTypes,
    Scale,
)

from dis_snek.models import Permissions

# async def read_file(filepath, mode):
#     async with aiofiles.open(filepath, mode=mode) as f:
#         await f.read()


# def read_file(filepath, mode='r'):
#     with open(filepath, mode=mode) as f:
#         file = f.read()
#     return json.loads(file)
    

class PhoneCall(Scale):
    def __init__(self, bot):
        self.bot = bot
        #TODO : this won't work need to write a function to open the file 
        #TODO : then JSON load US AIOFILES package to handle sync to ASYNC bs
        with open('./data/phone.json') as f:
            phone_list = json.loads(f.read())['phoneList']
        self.phonelist = phone_list


    @slash_command(
        name='addnumber',
        description='add a phone number to the call list'
    )
    @slash_option(
        name='number',
        description='phone number to be added',
        required=True,
        opt_type=OptionTypes.STRING
    )
    async def add_number(self, ctx: InteractionContext, number):
        print(self.phonelist)
        if number not in self.phonelist:
            self.phonelist.append(number)
            async with aiofiles.open('./data/phone.json', mode='w+') as f:
                data_json = json.dumps({'phoneList': self.phonelist})
                await f.write(data_json)

        await ctx.send('number added')

def setup(bot):
    PhoneCall(bot)



