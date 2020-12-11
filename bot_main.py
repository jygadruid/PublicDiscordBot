import discord
from discord.ext import commands
import time

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity = discord.Game('.survey option option'))


@client.event
async def on_error(event, *args, **kwargs):
    """
    Catches any exception that occurs during the bot's loop.
    If any exception is raised in ``on_error``, it will `not` be handled.
    The exception itself can be accessed from :class:`sys.exc_info`.
    Args:
        event:
            The name of the event that raised the exception.
        *args:
            The positional arguments for the event that raised the exception
        **kwargs:
             The keyword arguments for the event that raised the exception.
    """
    print("OH NO!, AN ERROR ;(")
    print("Error from:", event)
    print("Error context:", args, kwargs)

    from sys import exc_info

    exc_type, value, traceback = exc_info()
    print("Exception type:", exc_type)
    print("Exception value:", value)
    print("Exception traceback object:", traceback)


# bot invite = https://discord.com/oauth2/authorize?client_id=778071865326305290&permissions=8&scope=bot


@client.event
async def on_message(message):
    mSplit = message.content.split()
    if message.author != client.user:
        if message.content.startswith('.coolme'):
            await message.channel.send(f'**{message.author}** is very cool! :grinning:')
        # .survey <message>
        if message.content.startswith('.survey'):
            question = ' '.join(mSplit[1:])
            embed=discord.Embed(title="Survey", description=question)
            embed.add_field(name="Option 1", value="✔️", inline=True)
            embed.add_field(name="Option 2", value="❌", inline=True)
            sent = await message.channel.send(embed=embed)
            await sent.add_reaction("✔️")
            await sent.add_reaction("❌")
    await client.process_commands(message)


@client.command(aliases=['pong'])
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


# Amount is 6 instead of 5 because recent messages will also clear the command.
@client.command(aliases=['clear', 'clean'])
@commands.has_permissions(manage_messages=True)
async def _clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Cleared **{amount}** messages.')
    time.sleep(5)
    await ctx.channel.purge(limit=1)


@client.command()
async def whois(ctx):
    await ctx.send(f'You are **{ctx.author}**')


client.run('XXXXXXXX')