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

from twilio.rest import Client

from boto3 import session
from botocore.client import Config

from secrets import twilio_account_sid, twilio_auth_token, spaces_key, spaces_secret


spaces_session = session.Session()
spaces_client = Client('s3',
                        region_name='nyc3',
                        endpoint_url='https://jom-world-boss.nyc3.digitaloceanspaces.com',
                        aws_access_key_id=spaces_key,
                        aws_secret_access_key=spaces_secret
)       

twilio_client = Client(twilio_account_sid, twilio_auth_token)

class PhoneCall(Scale):
    def __init__(self, bot):
        self.bot = bot
        with open('./data/phone.json') as f:
            phone_list = json.loads(f.read())
        self.phonelist = phone_list       
        self.twilio = Client(twilio_account_sid, twilio_auth_token)

    def call_phone(self, number):
        call = self.twilio.calls.create(url='https://demo.twilio.com/welcome/voice/',
                        to=number,
                        from_='+19404128239')
        print(call.sid)        
    
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
        member_list = list(self.phonelist.keys())
        phone_list = list(self.phonelist.values())
        if ctx.author in member_list:
            await ctx.send('number already added')
        if number not in phone_list:
            if len(number) == 10:
                number = '1'+number
            number = '+'+number
            self.phonelist.update({str(ctx.author): number})
            async with aiofiles.open('./data/phone.json', mode='w+') as f:
                data_json = json.dumps({'phoneList': self.phonelist})
                await f.write(data_json)

            await ctx.send('number added')

    @slash_command(name='makecall')
    async def make_call(self, ctx:InteractionContext):
        for num in self.phonelist.values():
            self.call_phone(num)
        await ctx.send('call made')
        
def setup(bot):
    PhoneCall(bot)



