import discord
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import Bot

class Reload(commands.Cog, name="Reload"):
    """Module reload command"""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Admin")
    @commands.command()
    async def reload(self, ctx, module: str):
        """Reloads a module."""
        try:
            if module.startswith("Cog."):
                self.bot.reload_extension(module)
            else:
                self.bot.reload_extension(f"Cog.{module}")
        except Exception as e:
            print(e)
            print()
            embed = discord.Embed(title="Module error", description="Oops! That module doesn't exist.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Module reloaded", description="The module was reloaded successfully", color=discord.Color.gold())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Reload(bot))
