import discord
from discord.ext import commands
from utils.api_call import get_track_counts


class Streaming(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def streaming(self, ctx: commands.Context, *args: str) -> None:
        from_id: int = ctx.author.id
        _: str = ctx.author.name
        _: str = ctx.author.discriminator
        _: str = ctx.author.avatar

        track_counts = get_track_counts(from_id)

        return_str_list = []
        for track_count in track_counts:
            return_str_list.append(
                f"{track_count['track']['title']} : {track_count['streamingCount']}"
            )

        await ctx.reply("\n".join(return_str_list))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Streaming(bot))
