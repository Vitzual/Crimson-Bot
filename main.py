# import all needed imports
import discord
from discord.ext import commands
from discord.utils import get
import coc
import math
import traceback
import sys
import datetime

# Setup bot
TOKEN = "TOKEN HERE"  # Bot token -- used to push code to bot
bot = commands.Bot(command_prefix="!", description="Syntax: <needed> [optional]\nMade by Vitzual")
startup_extensions = ["Cog.reload"] # Load commands via COG

# Specify which clan to access (Crimson Frost)
clan_tags = ["#29U92UUYL"]

# Access the Clash of Clans API
coc_client = coc.login('USERNAME', 'PASSWORD', client=coc.EventsClient, key_names="crimson frost", key_count=1)

# On member join, grab information and send to channel
@coc_client.event
@coc.ClanEvents.member_join(tags=clan_tags)
async def on_clan_member_join(member, clan):
    
    player = await coc_client.get_player(member.tag)
    clan_obj = await coc_client.get_clan(clan.tag)
    
    # If town hall level less than 6, set level to 6 (for emoji)
    if player.town_hall < 6:
        THL = 6
    else:
        THL = player.town_hall
        
    # List of town halls
    th_emojis = ["<:TH6:794033498683998218>", "<:TH7:794032874953244674>", "<:TH8:794032875082219571>", "<:TH9:794034680122966067>", "<:TH10:794032874461855776>", "<:TH11:794032875083268116>", "<:TH12:794034330854096947>", "<:TH13:794033920688783366>"]
    
    # List of hero emojis
    hero_emojis = ["<:King:794101568664371222>", "<:Queen:794101569028358154>", "<:Warden:794101569141604352>", "<:Royal:794101568701202434>"]
    
    # Grab hero data from player object
    heroes, index = "", 0
    for scan in player.heroes:
        if scan.is_home_base:
            heroes += f"**({hero_emojis[index]})** {scan.name} level {scan.level}\n"
        index+=1
    if heroes == "":
        heroes = "No hero's unlocked"
    
    # Dictionary of league emojis 
    emojis = {
        "Unranked": "<:Unranked:794104498028019724>",
        "Bronze": "<:Bronze:794104498754814012>",
        "Silver": "<:Silver:794104498406555688>",
        "Gold": "<:Gold:794104498095783957>",
        "Crystal": "<:Crystal:794104498213486603>",
        "Master": "<:Master:794104498552438815>",
        "Champion": "<:Champion:794104498246254603>",
        "Titan": "<:Titan:794104498465406978>",
        "Legend": "<:Legend:794112575335038976>"
    }
    
    emoji = emojis[member.league.name.split(" ", 1)[0]]
    
    # Make thing message thing
    message = f"Go welcome {player.name} to the clan!\n" \
          f"\n**Player stats:**" \
          f"\n**({th_emojis[player.town_hall-6]})** TH level {player.town_hall}" \
          f"\n**(<:XP:794101135437725709>)** Level {player.exp_level}" \
          f"\n**(<:Trophy:794097753982238721>)** {player.trophies} trophies" \
          f"\n**({emoji})** {player.league.name}" \
          f"\n**(<:Star:794122648614862878>)** {player.war_stars} war stars" \
          f"\n\n**Hero stats:**" \
          f"\n{heroes}" \
          f"\n**Clash of stats profile:**" \
          f"\nhttps://www.clashofstats.com/players/{player.tag.strip('#')}"
    
    # Set the embed
    embed = discord.Embed(title=f"<:Joined:794127183559917568> New Player | {player.name}", description=message, color=discord.Color.red())
    embed.set_footer(text=f"Joined {clan_obj.name} • {datetime.datetime.now().strftime('%b %d, %Y')}", icon_url=clan_obj.badge.small)
    
    # Send message to a channel or something lmao fuck idk
    channel = bot.get_channel(793613833314762828)
    await channel.send(embed=embed)

# Display connected bot
@bot.event 
async def on_ready():
    print(f"Connected {bot.user}")  # Send message on connection

# On member join event, send message to channel
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(793613832945139720)
    description = f"Welcome to **Crimson Frost™**, {member.mention}! Make sure to read the <#793613832945139721> and the DM sent to you to know more about us. If you want to join the clan, please go to <#793613833167306772> and post an image of your profile and your base. We will get back to you in regards to joining the clan."
    await channel.send(description)

# On error, print to screen
@bot.event
async def on_command_error(ctx, error):
    # If command has local error handler, return
    if hasattr(ctx.command, 'on_error'):
        return

    # Get the original exception
    error = getattr(error, 'original', error)

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=f"Argument error", description=f"You forgot to all the variables! Check what you need with {bot.command_prefix}help {ctx.command}`", color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
        embed = discord.Embed(title=f"Permission error", description='I need the **{}** permission(s) to run this command.'.format(fmt), color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.DisabledCommand):
        embed = discord.Embed(title=f"Disabled error", description="This command has been disabled", color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"Woah there cowboy!", description=f"That command has a cooldown!", color=discord.Color.red())
        embed.set_footer(text=f"Please try again in {format(math.ceil(error.retry_after))}s")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
        embed = discord.Embed(title=f"Permission error",
                              description=f"{_message}",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    if isinstance(error, commands.NoPrivateMessage):
        try:
            embed = discord.Embed(title=f"DM error",
                                  description="This command cannot be sued in direct messages",
                                  color=discord.Color.red())
            embed.set_footer(text=f"{error}")
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            pass
        return

    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(title=f"Permission error",
                              description=f"You do not have permission to use this command",
                              color=discord.Color.red())
        embed.set_footer(text=f"{error}")
        await ctx.send(embed=embed)
        return

    # ignore all other exception types, but print them to stderr
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

if __name__ == "__main__":  # When script is loaded, this will run
  bot.remove_command("help")
  for extension in startup_extensions:
    try:
      bot.load_extension(extension)  # Loads cogs successfully
    except Exception as e:
      exc = '{}: {}'.format(type(e).__name__, e)
      print('Failed to load extension {}\n{}'.format(extension, exc))  # Failed to load cog, with error

bot.run(TOKEN)
