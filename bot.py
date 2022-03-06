import dis_snek
import logging
from secrets import token

from dis_snek import const, listen, slash_command, InteractionContext, Embed
from dis_snek.client import Snake
from dis_snek.models import ComponentContext, Intents
from dis_snek.api.events import Component



logging.basicConfig()
cls_log = logging.getLogger(const.logger_name)
cls_log.setLevel(logging.DEBUG)

bot = Snake(intents=Intents.DEFAULT, sync_interactions=True, asyncio_debug=True)

class Bot(Snake):
    def __init__(self):
        super().__init__(
            intents=Intents.DEFAULT | Intents.GUILD_MEMBERS | Intents.MESSAGES,
            sync_interactions = True,
            delete_unused_application_cmds=True,
            asyncio_debug=True,
            activity="with sneks",
            debug_scope=949771069798113300,
            fetch_members=True,
        )
    
    @listen()
    async def on_ready(self):
        print("Ready")
        print(f"This bot is owned by {bot.owner}")
        print(f'{bot.user} logged in')
    

    @listen()
    async def on_guild_create(event):
        print(f"guild created : {event.guild.name}")


    @listen()
    async def on_message_create(event):
        print(f"message received: {event.message.content}")


    @listen()
    async def on_component(event: Component):
        ctx = event.context
        await ctx.edit_origin("test")


    @slash_command("help", "Basic instructions and what this bot is")
    async def help(ctx: InteractionContext):
        embed = Embed(
            "Starboard Help",
            "While the name of the bot is Popularity Contest, thats basically what a starboard is. A few of the commands I have or will be adding are listed below. 💫",
            color="#FAD54E",
        )
        embed.add_field("setup", "Sets up the starboard for the server")
        embed.add_field(
            "More Info",
            f"No feature is blocked behind a vote wall, but if you are feeling kind could you [upvote](https://top.gg/bot/{bot.user.id}/vote) \👉\👈",
        )
        await ctx.send(embeds=[embed])


    @slash_command("privacy", "Privacy Policy")
    async def privacy(ctx: InteractionContext):
        embed = Embed(
            "Privacy Policy",
            """Your data is important and we take your privacy seriously. This is a simple privacy policy that explains what we do with your data and how we use it. \n
            When you set up the bot we collect:
            - Guild ID
            - Starboard Channel ID
            For starred messages the following is stored:
            - The message ID
            - The message Channel ID
            - The message author ID
            - The amount of stars
            - IDs of the users who have starred the message
            - Starboard post ID
            
            We never store message content, only IDs and counts. 
            All of the code is open source and can be found [here](https://github.com/Wolfhound905/popularity-contest)
            If you are concerned please DM `Wolfhound905#1234`""",
        )
        await ctx.send(embed=embed, ephemeral=True)



bot = Bot()
bot.g_id = 949771069798113300

bot.grow_scale('commands.world_boss_timers')
bot.start(token)