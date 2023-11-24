import os
from discord.ext import commands
<<<<<<< HEAD
from utils.api_call import check_user_account, get_user_inbox_account, create_inbox_account, create_social_account
=======
from utils.api_call import check_user_account, get_user_inbox_account, create_inbox_account, create_social_account, register_sns
>>>>>>> d5e9a38 (Add: !register command)


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def register(self, ctx) -> None:
        from_id = str(ctx.author.id)
        from_name = ctx.author.name
        from_discriminator = ctx.author.discriminator
        from_avatar = ctx.author.avatar

        social_account_pub_key, is_inbox =check_user_account(from_id)
        
        if social_account_pub_key != "" and is_inbox:
            inbox_address = get_user_inbox_account(from_id)
            
            await ctx.reply(
                f":genie:: Hey {from_name}! You already registered genie. Your inbox wallet address is {inbox_address}. This message will be deleted after 10 seconds.",
                delete_after=10.0,
            )

            return
        
        await ctx.reply(
                f":genie:: Please wait.",
                delete_after=10.0,
            )

        if social_account_pub_key != "":
            register_sns("Solana", social_account_pub_key, from_id, from_name + '#' + from_discriminator)
            inbox_address = create_inbox_account(from_id, "Solana")
            
            await ctx.reply(
                f":genie:: Hey {from_name}! Your inbox wallet is registered .\nAddress: {inbox_address}.\nThis message will be deleted after 10 seconds.",
            delete_after=10.0,
            )

        else:
            social_account_pub_key = create_social_account(from_name + '#' + from_discriminator)
            register_sns("Solana", social_account_pub_key, from_id, from_name + '#' + from_discriminator)
            inbox_address = create_inbox_account(from_id, "Solana")

            await ctx.reply(
                f":genie:: Hey {from_name}! Your genie wallet is registered .\n**Inbox Address: {inbox_address}**\nThis message will be deleted after 10 seconds.",
            delete_after=10.0,
            )

        return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Register(bot))
