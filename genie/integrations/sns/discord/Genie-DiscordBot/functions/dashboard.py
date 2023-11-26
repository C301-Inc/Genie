import asyncio
import os
import discord
from discord.ext import commands
from utils.api_call import check_user_account, get_user_inbox_account, get_user_tokens, get_user_nfts, get_user_coin_tx_history, get_user_nft_tx_history


class Dashboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def dashboard(self, ctx, *args) -> None:
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
            f":genie:: Please wait...",
            delete_after=20.0
        )

        token_value_list, token_ticker_list, token_address_list = get_user_tokens(from_id, "Solana") 
        nft_name_list, nft_address_list = get_user_nfts(from_id, "Solana")  
        
        text += "**Token Holdings**\n"
        if len(token_value_list) == 0:
            text += "None\n" 
        else:
            for i in range(len(token_value_list)):
                text += token_ticker_list[i]
                text += " : "
                text += str(token_value_list[i])
                text += "\n"

        text += "**NFT Holdings**\n"
        if len(nft_name_list) == 0:
            text += "None\n"
        else:
            for i in range(len(nft_name_list)):
                text += nft_name_list[i]
                text += " ("
                text += nft_address_list[i]
                text += ") : "
                text += "1\n"

        text += "**Token Tx History**\n"
        coin_txs = get_user_coin_tx_history(from_id)
        if len(coin_txs) == 0:
            text += "None\n"
        else:
            for coin_tx in coin_txs:
                if coin_tx['isSent']:
                    text += f"<@{from_id}> -> <@{coin_tx['targetSnsDiscriminator']}> ({coin_tx['amount']} {coin_tx['coin']['ticker']}) [Link](https://solana.fm/tx/{coin_tx['txHash']}?cluster=devnet-solana)\n"
                else:
                    text += f"<@{coin_tx['targetSnsDiscriminator']}> -> <@{from_id}> ({coin_tx['amount']} {coin_tx['coin']['ticker']} [Link](https://solana.fm/tx/{coin_tx['txHash']}?cluster=devnet-solana)\n"

        text += "**NFT Tx History**\n"
        nft_txs = get_user_nft_tx_history(from_id)
        if len(nft_txs) == 0:
            text += "None\n"
        else:
            for nft_tx in nft_txs:
                if nft_tx['isSent']:
                    text += f"<@{from_id}> -> <@{nft_tx['targetSnsDiscriminator']}> (1 {nft_tx['NFT']['name']} [Link](https://solana.fm/tx/{nft_tx['txHash']}?cluster=devnet-solana)\n"
                else:
                    text += f"<@{nft_tx['targetSnsDiscriminator']}> -> <@{from_id}> (1 {nft_tx['NFT']['name']} [Link](https://solana.fm/tx/{nft_tx['txHash']}?cluster=devnet-solana)\n"

        message = await ctx.reply(
            text,
            delete_after=60.0
        )
        await message.edit(suppress=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Dashboard(bot))
