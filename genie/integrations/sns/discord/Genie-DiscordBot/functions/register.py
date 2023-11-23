import os
from discord.ext import commands
from utils.api_call import check_user_account, get_user_inbox_account, create_inbox_account, create_social_account


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def register(self, ctx) -> None:
        from_id = ctx.author.id
        from_name = ctx.author.name
        from_discriminator = ctx.author.discriminator
        from_avatar = ctx.author.avatar
        
        is_social_account, is_inbox =check_user_account(from_id)
        
        if is_social_account and is_inbox:
            inbox_address = get_user_inbox_account(from_id)
            await ctx.reply(
                f":genie:: Hey {from_name}! You already registered genie. Your inbox wallet address is {inbox_address}. This message will be deleted after 10 seconds.",
                delete_after=10.0,
            )
        
        if is_social_account:
            inbox_address = create_inbox_account(from_id, "Solana")
            await ctx.reply(
                f":genie:: Hey {from_name}! Your inbox wallet is registered .\nAddress: {inbox_address}.\nThis message will be deleted after 10 seconds.",
            delete_after=10.0,
            )
        else:
            create_social_account(from_name + '#' + from_discriminator)
            inbox_address = create_inbox_account(from_id, "Solana")
            await ctx.reply(
                f":genie:: Hey {from_name}! Your genie wallet is registered .\nInbox Address: {inbox_address}.\nThis message will be deleted after 10 seconds.",
            delete_after=10.0,
            )

        return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Register(bot))
