from datetime import datetime, timedelta, tzinfo, timezone
from random import choice
from tokenize import group
import json

import pytz


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


class PhoneCall(Scale):
    def __init__(self, bot):
        self.bot = bot
        #TODO : this won't work need to write a function to open the file 
        #TODO : then JSON load US AIOFILES package to handle sync to ASYNC bs
        self.phonelist = json.load('../data/phone.json')

    # @slash_command(
    #     name='phonecall',
    #     description='call all the listed numbers that a boss is up'
    # )
    # async def phone_call(self, ctx: InteractionContext):
    #     pass
    
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
        if number not in self.phonelist:
            self.phonelist.append(number)
            json.dump({'phoneList': self.phonelist},'../data/phone.json')
        await ctx.send('number added')

def setup(bot):
    PhoneCall(bot)



