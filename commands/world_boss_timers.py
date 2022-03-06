from datetime import datetime, timedelta, tzinfo, timezone
from tokenize import group

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



class WorldBossTimers(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = pytz.timezone('US/Eastern')
        self.bosses = ['Azuregos','Kazzak', 'Green Dragons']
        self.timers = {}



    @slash_command(
        name='wboss',
        description='World Boss related bot commands',
        sub_cmd_name='timers',
        sub_cmd_description='get current world boss windows'
        )
    async def timer_command(self, ctx: InteractionContext):
        response = '```Servertime: {servertime:%A %B %d %H:%M}\n{lines}```'
        line_fmt = '{}:\n \t START: {:%A %B %d %H:%M}\n \t END: {:%A %B %d %H:%M}\n\t {}'
        cur_dt = datetime.now(self.timezone)
        timer_values = []
        for key in self.timers.keys():
            start_dt = self.timers[key]['start']
            end_dt = self.timers[key]['end']
            additional = ''
            if cur_dt < start_dt:
                diff = start_dt-cur_dt
                d = diff.days
                h = diff.seconds // 3600
                m = diff.seconds % 3600 // 60
                additional = 'Window Opens in {}d {}h {}m'.format(d, h, m)
            elif cur_dt <= end_dt:
                diff = end_dt-cur_dt
                d = diff.days
                h = diff.seconds // 3600
                m = diff.seconds % 3600 // 60
                additional = 'Window Closes in {}d {}h {}m'.format(d, h, m)
            else:
                additional = 'Window has passed'
            tmp_line = line_fmt.format(key, start_dt, end_dt, additional)
            timer_values.append((tmp_line, start_dt))
        timer_values.sort(key=lambda x: x[1])
        timer_lines = [line for line, _ in timer_values]
        await ctx.send(response.format(
            servertime=cur_dt, lines='\n\n'.join(timer_lines)))


    @slash_command(
        name='wboss',
        description='World Boss related bot commands',
        sub_cmd_name='reset',
        sub_cmd_description='set world boss windows after a server restart'        
    )
    async def server_restart(self, ctx: InteractionContext):
        cur_dt = datetime.now(self.timezone)
        start = cur_dt + timedelta(hours=12)
        end = cur_dt + timedelta(hours=36)
        for boss in self.bosses:
            self.timers.update({boss: {'start': start, 'end': end}})
        
        await ctx.send("Boss Timers have been updated based on a server restart")


def setup(bot):
    WorldBossTimers(bot)
    