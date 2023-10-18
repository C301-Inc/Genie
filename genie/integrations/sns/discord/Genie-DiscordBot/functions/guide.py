import discord

from discord.ext import commands


class Guide(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def guide(self, ctx: commands.Context, *args: str) -> None:
        from_id: int = ctx.author.id
        from_name: str = ctx.author.name
        from_discriminator: str = ctx.author.discriminator
        from_avatar: str = ctx.author.avatar

        command_description = [
            "**!register**\nCommand to create Genie wallet.",
            "**!dashboard**\nCommand to display the assets and tx history.",
            "**!send**\nCommand to send assets. Type '!send token/nft @username' to use.",
            "**!withdraw**\nCommand to withdraw assets in Genie wallet. Type '!withdraw [wallet address]' to use.",
        ]

        ret_text = '\n'.join(command_description)

        await ctx.reply(f"**:genie:Genie bot commands:genie:**\n\n{ret_text}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Guide(bot))
