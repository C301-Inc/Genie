import os
import discord
from discord.ext import commands
from utils.api_call import check_user_account


class Deposit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def deposit(self, ctx, *args) -> None:
        from_id = ctx.author.id
        from_name = ctx.author.name
        from_discriminator = ctx.author.discriminator
        from_avatar = ctx.author.avatar

        social_account_pub_key, is_inbox =check_user_account(from_id)
        text = ""

        if social_account_pub_key == "" or not is_inbox:
            await ctx.reply(
                f":genie:: Hey {from_name}! Please use !register command to create your genie wallet. This message will be deleted after 10 seconds.",
                delete_after=10.0,
            )

            return

        await ctx.reply(
            f":genie:: Click [Link]({os.environ.get('DEPOSIT_URL')}) to deposit in your Genie wallet."
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Deposit(bot))
