from Other.variables import Variables
from Other.private import Private
from gpiozero import CPUTemperature


async def delete(context, msgID):
    if context.message.author.id in Private.DEV_IDS.keys():
        msg = await context.message.channel.fetch_message(msgID)
        await msg.delete()
        await context.message.delete()

async def say(context):
    if context.message.author.id in Private.DEV_IDS.keys():
        await context.channel.send(context.message.content[len("?say "):])
        await context.message.delete()

async def temp(ctx=None):
    if ctx.message.author.id in Private.DEV_IDS.keys():
        await ctx.channel.send(str(CPUTemperature().temperature) + "°C")

