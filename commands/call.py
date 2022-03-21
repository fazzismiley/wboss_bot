import os
import json
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

# from secrets import twilio_account_sid, twilio_auth_token, spaces_key, spaces_secret

#cloud
TWILIO_ACCNT_SID = os.environ.get('TWILIO_ACCNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
SPACES_KEY = os.environ.get('SPACES_KEY')
SPACES_SECRET = os.environ.get('SPACES_SECRET')

#local
# TWILIO_ACCNT_SID = twilio_account_sid
# TWILIO_AUTH_TOKEN = twilio_auth_token
# SPACES_KEY = spaces_key
# SPACES_SECRET = spaces_secret

spaces_session = session.Session()
spaces_client = spaces_session.client('s3',
                        region_name='nyc3',
                        endpoint_url='https://nyc3.digitaloceanspaces.com',
                        aws_access_key_id=SPACES_KEY,
                        aws_secret_access_key=SPACES_SECRET
)       

twilio_client = Client(TWILIO_ACCNT_SID, TWILIO_AUTH_TOKEN)

class PhoneCall(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.bucket = spaces_client
        self.twilio = twilio_client

    def load_phonelist(self):

        content_obj = self.bucket.get_object(Bucket='jom-world-boss', Key='phone.json')
        file_data = content_obj['Body'].read().decode('utf-8')
        json_data = json.loads(file_data)
        return json_data

    def write_phonelist(self,new_phone_list):
        content_obj = self.bucket.put_object(Bucket='jom-world-boss',
                                            Key='phone.json',
                                            Body=(bytes(json.dumps(new_phone_list).encode('UTF-8'))),
                                            ACL='private')

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
        if len(number) == 10:
                number = '1'+number
        number = '+'+number
        phonebook = self.load_phonelist()
        member_list = list(phonebook.keys())
        number_list = list(phonebook.values())
        if ctx.author in member_list:
            await ctx.send('User has a number asscoiated with them')
        if number in number_list:
            await ctx.send('Number already entered')

        
        phonebook.update({str(ctx.author): number})
        self.write_phonelist(phonebook)
        await ctx.send('number added')

    @slash_command(name='makecall')
    async def make_call(self, ctx:InteractionContext):
        phonelist= self.load_phonelist()
        count = 0
        for num in list(phonelist.values()):
            self.call_phone(num)
            count += 1
        await ctx.send(f'{count} calls made')
        
def setup(bot):
    PhoneCall(bot)



